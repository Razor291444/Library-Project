"""AI23 - Projet A23: Database file, contains the database class"""

from enum import Enum
from datetime import datetime, timedelta

import psycopg2 as pg
from psycopg2 import sql


class LibraryDatabaseException(Exception):
    """Exception raised by the LibraryDatabase class"""


class Account(Enum):

    """Enum for the account type""" 

    Adherent = "Adherent"
    Personnel = "Personnel"
    Administrateur = "Administrateur"


class LibraryDatabase:
    """Interact with the PostGres SQL database"""

    def __init__(self, host, port, db_name, user, password):
        """Connect to the database"""
        try:
            self.conn = pg.connect(host=host,
                                   port=port,
                                   dbname=db_name,
                                   user=user,
                                   password=password)
            self.cur = self.conn.cursor()

        except pg.OperationalError as err:
            raise LibraryDatabaseException("Unable to connect to the database") from err


    def __del__(self):
        """Close the connection"""
        # Class destructor
        try:
            self.cur.close()
            self.conn.close()
        except pg.OperationalError as err:
            raise LibraryDatabaseException("Unable to close the database connection") from err

    def login(self, login: str, password:str) -> bool:

        """Check if the username and password are correct"""
        try:
            self.cur.execute(f"SELECT * FROM utilisateur WHERE \
                               login='{login}' AND \
                               mot_de_passe='{password}'")
            return self.cur.fetchone() is not None

        except pg.OperationalError as err:
            raise LibraryDatabaseException("Unable to login") from err


    def get_account_type(self, username: str) -> Account:

        """Get the account type of a user"""

        try:
            query = sql.SQL("""
                SELECT type FROM utilisateur
                WHERE login={username}
            """).format(username=sql.Literal(username))

            self.cur.execute(query)
            result = self.cur.fetchone()

            if result:
                account_type_str = result[0]
                return Account[account_type_str]
            else:
                print(f"Error: User '{username}' not found.")
                return None

        except pg.OperationalError as err:
            raise LibraryDatabaseException("Unable to get account type") from err


    def get_ressources(self, resource_name: str, ressource_type="", only_available=False) -> [str]:
        """Get resources by name, type, and availability"""

        try:
            query = sql.SQL("""
                SELECT DISTINCT on (r.code)
                    r.code AS ressource_code, r.titre, r.date_apparition, r.genre, r.editeur, r.prix, r.code_classification, r.type, e.etat, e.code AS code_exemplaire, ri.imageUrl
                FROM ressource r
                JOIN exemplaire e ON r.code = e.ressource
                JOIN ressourceimage ri ON r.code = ri.ressource
                LEFT JOIN VuePretsEnCours v ON e.code = v.code_exemplaire
                WHERE r.titre ILIKE {resource_name} AND
                    (r.type::text ILIKE {ressource_type} AND (NOT {only_available} OR v.pret_code IS NULL));
            """).format(
                resource_name=sql.Literal(f'%{resource_name}%'),
                ressource_type=sql.Literal(f'%{ressource_type}%'),
                only_available=sql.SQL('TRUE' if only_available else 'FALSE')
            )

            self.cur.execute(query)
            available_resources = self.cur.fetchall()

            if available_resources:
                return available_resources
            else:
                return None

        except pg.OperationalError as err:
            raise LibraryDatabaseException("Unable to get resources") from err


    def get_user_infos(self, login: str) -> dict:
        """Get all information of a user by login"""

        try:
            query = sql.SQL("""
                SELECT nom, prenom, email, adresse, type FROM utilisateur
                WHERE login={login}
            """).format(login=sql.Literal(login))

            self.cur.execute(query)
            result = self.cur.fetchone()

            if result:
                columns = [desc[0] for desc in self.cur.description]
                user_info = dict(zip(columns, result))
                return user_info

            else:
                print(f"Error: User '{login}' not found.")
                return None

        except pg.OperationalError as err:
            raise LibraryDatabaseException("Unable to get user information") from err


    def get_ressource_infos(self, resource_code: str) -> dict:
        """Get all information of a resource by code"""

        try:
            query = sql.SQL("""
                SELECT r.*
                FROM ressource r
                WHERE r.code={resource_code}
            """).format(resource_code=sql.Literal(resource_code))

            self.cur.execute(query)
            result = self.cur.fetchone()

            if result:
                columns = [desc[0] for desc in self.cur.description]
                ressource_info = dict(zip(columns, result))
                return ressource_info

            else:
                print(f"Error: Resource '{resource_code}' not found.")
                return None

        except pg.OperationalError as err:
            raise LibraryDatabaseException("Unable to get resource information") from err


    def get_resource_contributors(self, resource_code: str) -> [str]:
        """Get all contributors of a resource by code"""

        try:
            query = sql.SQL("""
                SELECT c.*, cl.*, cf.*, com.*,
                    CASE
                        WHEN cl.livre IS NOT NULL THEN 'Livre'
                        WHEN cf.film IS NOT NULL THEN 'Film'
                        WHEN com.oeuvre_musicale IS NOT NULL THEN 'OeuvreMusicale'
                        ELSE NULL
                    END AS type_oeuvre
                FROM contributeur c
                LEFT JOIN contributionlivre cl ON c.id = cl.contributeur
                LEFT JOIN contributionfilm cf ON c.id = cf.contributeur
                LEFT JOIN contributionoeuvremusicale com ON c.id = com.contributeur
                WHERE
                    cl.livre = %s OR
                    cf.film = %s OR
                    com.oeuvre_musicale = %s
            """)

            self.cur.execute(query, (resource_code, resource_code, resource_code))
            result = self.cur.fetchall()

            if result:
                # Do not return 'null' values (null can be in each column of the result)
                contributors = []
                for row in result:
                    contributors.append([col for col in row if col is not None])

                # If the ressource is a movie 
                if contributors[0][-1] == 'Film':
                    results = []
                    for row in contributors:
                        results.append(f"{row[2]} {row[1]} ({row[3]}) - {row[7]}")

                # If the ressource is a book
                elif contributors[0][-1] == 'Livre':
                    # Add the role of the contributor
                    results = []
                    for row in contributors:
                        results.append(f"{row[2]} {row[1]} ({row[3]})")

                # If the ressource is a music
                elif contributors[0][-1] == 'OeuvreMusicale':            
                    results = []
                    for row in contributors:
                        results.append(f"{row[2]} {row[1]} ({row[3]}) - {row[7]}")

                return results

            else:
                print(f"Error: Resource '{resource_code}' not found.")
                return None

        except pg.OperationalError as err:
            raise LibraryDatabaseException("Unable to get resource contributors") from err


    def get_resource_copies(self, resource_code: str) -> [str]:
        """Get all copies of a resource by code with availability status"""

        try:
            query = sql.SQL("""
            SELECT
                E.code AS code_exemplaire,
                R.titre AS ressource_titre,
                CASE
                    WHEN E.code IN (SELECT code_exemplaire FROM VuePretsEnCours) THEN 'En cours de prêt'
                    ELSE 'Disponible'
                END AS disponibilite
            FROM
                Exemplaire E
            JOIN
                Ressource R ON E.ressource = R.code
            WHERE
                E.ressource = {resource_code}
            """).format(resource_code=sql.Literal(resource_code))

            self.cur.execute(query)
            result = self.cur.fetchall()

            if result:
                return result
            else:
                print(f"Error: Resource '{resource_code}' not found.")
                return None

        except pg.OperationalError as err:
            raise LibraryDatabaseException("Unable to get resource copies with availability status") from err


    def get_users(self) -> [str]:
        """Get all users"""

        try:
            query = sql.SQL("""
                SELECT login, nom, prenom, email, adresse, type FROM utilisateur
            """)

            self.cur.execute(query)
            result = self.cur.fetchall()

            if result:
                return result
            else:
                print("Error: No users found.")
                return None

        except pg.OperationalError as err:
            raise LibraryDatabaseException("Unable to get users") from err


    def create_user(self, login, password, user_type, nom, prenom, adresse, email, date_naissance, telephone=1234):
        """Create a new user by admin"""
        try:
            # Insert into Utilisateur table
            utilisateur_query = sql.SQL("""
                INSERT INTO utilisateur (login, mot_de_passe, nom, prenom, adresse, email, type)
                VALUES ({}, {}, {}, {}, {}, {}, {})
                RETURNING login
            """).format(
                sql.Literal(login),
                sql.Literal(password),
                sql.Literal(nom),
                sql.Literal(prenom),
                sql.Literal(adresse),
                sql.Literal(email),
                sql.Literal(user_type)
            )

            self.cur.execute(utilisateur_query)

            adherent_query = sql.SQL("""
                INSERT INTO adherent (login, date_naissance, telephone, status)
                VALUES ({}, {}, {}, {})
                RETURNING login
            """).format(
                sql.Literal(login),
                sql.Literal(date_naissance),
                sql.Literal(telephone),
                sql.Literal('Actif')  # Assuming a default status for a new adherent
            )

            self.cur.execute(adherent_query)
            self.conn.commit()

        except pg.OperationalError as err:
            # Rollback in case of an error
            self.conn.rollback()
            raise LibraryDatabaseException(f"Error: Unable to create user - {err}") from err



    def add_loan(self, adherent_username, exemplaire_code, loan_duration):
        """Add a new loan"""
        try:
            current_date = datetime.now().date()
            return_date = current_date + timedelta(days=int(loan_duration))

            query = sql.SQL("""
                INSERT INTO pret (adherent, exemplaire, date_pret, duree, date_rendu)
                VALUES ({adherent_username}, {exemplaire_code}, {current_date}, {loan_duration}, {return_date})
            """).format(
                adherent_username=sql.Literal(adherent_username),
                exemplaire_code=sql.Literal(exemplaire_code),
                current_date=sql.Literal(current_date),
                loan_duration=sql.Literal(loan_duration),
                return_date=sql.Literal(return_date)
            )
            self.cur.execute(query)
            self.cur.execute("COMMIT")
            print("Loan added successfully.")

        except pg.OperationalError as err:
            print(f"Error: Unable to add loan - {err}")

    # def return_resource(self, loan_code, resource_condition):
    #     """Return a resource and handle related actions"""
    #     try:
    #         current_date = datetime.now().date()

    #         # Update loan status to the current date
    #         update_loan_query = sql.SQL("""
    #             UPDATE pret
    #             SET date_rendu={current_date}
    #             WHERE code={loan_code}
    #         """).format(current_date=sql.Literal(current_date), loan_code=sql.Literal(loan_code))
    #         self.cur.execute(update_loan_query)

    #         # Check resource condition and create a sanction if damaged
    #         if resource_condition == 'Abime':
    #             create_sanction_query = sql.SQL("""
    #                 INSERT INTO sanction (adherent, debut)
    #                 SELECT adherent, {current_date}
    #                 FROM pret
    #                 WHERE code={loan_code}
    #             """).format(current_date=sql.Literal(current_date), loan_code=sql.Literal(loan_code))
    #             self.cur.execute(create_sanction_query)

    #             # Update resource status to 'Abime' if needed
    #             update_resource_status_query = sql.SQL("""
    #                 UPDATE ressource
    #                 SET etat='Abime'
    #                 FROM pret
    #                 WHERE ressource.code = pret.exemplaire
    #                 AND pret.code={loan_code}
    #             """).format(loan_code=sql.Literal(loan_code))
    #             self.cur.execute(update_resource_status_query)

    #         print("Resource returned successfully.")
    #     except pg.OperationalError as err:
    #         print(f"Error: Unable to return resource - {err}")

    def is_eligible_to_borrow(self, adherent_username):
        """Check if an adherent is eligible to borrow"""

        pret_en_cours_query = sql.SQL("""
            SELECT COUNT(*) FROM VuePretsEnCours
            WHERE adherent_login={adherent_username}
        """).format(adherent_username=sql.Literal(adherent_username))
        self.cur.execute(pret_en_cours_query)

        pret_en_cours_count = self.cur.fetchone()[0]

        print(f"Current loans: {pret_en_cours_count}")

        return pret_en_cours_count <= 3
