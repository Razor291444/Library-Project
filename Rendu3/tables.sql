CREATE TYPE enum_oeuvre AS ENUM('Livre', 'OeuvreMusicale', 'Film');

CREATE TABLE Ressource (
    code SERIAL PRIMARY KEY,
    titre VARCHAR(255),
    date_apparition DATE,
    genre VARCHAR(50),
    editeur VARCHAR(100),
    prix DECIMAL(10, 2),
    code_classification INT,
    type enum_oeuvre,
    CHECK (type IS NOT NULL)
);


CREATE TABLE Film (
    code INT PRIMARY KEY,
    langue VARCHAR(50),
    duree INT,
    synopsis TEXT,
    FOREIGN KEY (code) REFERENCES Ressource(code)
);

CREATE TABLE Livre (
    code INT PRIMARY KEY,
    ISBN VARCHAR(20),
    resume TEXT,
    langue VARCHAR(50),
    FOREIGN KEY (code) REFERENCES Ressource(code)
);

CREATE TABLE OeuvreMusicale (
    code INT PRIMARY KEY,
    duree INT,
    FOREIGN KEY (code) REFERENCES Ressource(code)
);

CREATE TYPE enum_etat_exemplaire AS ENUM('Neuf', 'Bon', 'Abime', 'Perdu');

CREATE TABLE Exemplaire (
    code SERIAL PRIMARY KEY,
    ressource INT,
    etat enum_etat_exemplaire,
    FOREIGN KEY (ressource) REFERENCES Ressource(code) ON DELETE CASCADE,
    CHECK (ressource IS NOT NULL)
);

CREATE TYPE enum_personnel AS ENUM('Adherent', 'Personnel', 'Administrateur');

CREATE TABLE Utilisateur (
    login VARCHAR(50) PRIMARY KEY,
    mot_de_passe VARCHAR(255) NOT NULL,
    nom VARCHAR(50),
    prenom VARCHAR(50),
    adresse VARCHAR(255),
    email VARCHAR(100),
    type enum_personnel NOT NULL,
    CHECK (mot_de_passe IS NOT NULL),
    CHECK (type IS NOT NULL)
);

CREATE TYPE enum_statut_adherent AS  ENUM('Actif', 'Supprime', 'Blacklist');

CREATE TABLE Adherent (
    login VARCHAR(50) PRIMARY KEY,
    date_naissance DATE,
    telephone VARCHAR(20),
    status enum_statut_adherent,
    FOREIGN KEY (login) REFERENCES Utilisateur(login) ON DELETE CASCADE
);

CREATE TABLE Sanction (
    id SERIAL PRIMARY KEY,
    adherent VARCHAR(50),
    debut DATE NOT NULL,
    fin DATE,
    FOREIGN KEY (adherent) REFERENCES Adherent(login) ON DELETE CASCADE,
    CHECK (debut IS NOT NULL)
);

CREATE TABLE Pret (
    code SERIAL PRIMARY KEY,
    adherent VARCHAR(50),
    exemplaire INT,
    date_pret DATE NOT NULL,
    duree INT,
    date_rendu DATE,
    FOREIGN KEY (adherent) REFERENCES Adherent(login) ON DELETE CASCADE,
    FOREIGN KEY (exemplaire) REFERENCES Exemplaire(code) ON DELETE CASCADE,
    CHECK (date_pret IS NOT NULL)
);

CREATE TABLE Contributeur (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50),
    prenom VARCHAR(50),
    date_naissance DATE,
    nationalite VARCHAR(50)
);

CREATE TYPE enum_type_contri_oeuvre_musical AS ENUM('Interprete', 'Compositeur', 'InterpreteCompositeur');

CREATE TABLE ContributionOeuvreMusicale (
    contributeur INT,
    oeuvre_musicale INT,
    type enum_type_contri_oeuvre_musical NOT NULL,
    PRIMARY KEY (contributeur, oeuvre_musicale),
    FOREIGN KEY (contributeur) REFERENCES Contributeur(id) ON DELETE CASCADE,
    FOREIGN KEY (oeuvre_musicale) REFERENCES OeuvreMusicale(code) ON DELETE CASCADE,
    CHECK (type IS NOT NULL)
);

CREATE TYPE enum_type_contri_film AS ENUM('Acteur', 'Realisateur', 'ActeurRealisateur');

CREATE TABLE ContributionFilm (
    contributeur INT,
    film INT,
    type  enum_type_contri_film NOT NULL,
    PRIMARY KEY (contributeur, film),
    FOREIGN KEY (contributeur) REFERENCES Contributeur(id) ON DELETE CASCADE,
    FOREIGN KEY (film) REFERENCES Film(code) ON DELETE CASCADE,
    CHECK (type IS NOT NULL)
);

CREATE TABLE ContributionLivre (
    contributeur INT,
    livre INT,
    PRIMARY KEY (contributeur, livre),
    FOREIGN KEY (contributeur) REFERENCES Contributeur(id) ON DELETE CASCADE,
    FOREIGN KEY (livre) REFERENCES Livre(code) ON DELETE CASCADE
);

-- Partage des tables à l'utilisateur AI23A025

GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE ContributionLivre, ContributionFilm, 
ContributionOeuvreMusicale, Contributeur, Pret, Sanction, Adherent, Utilisateur, 
Exemplaire, OeuvreMusicale, Livre, Film, Ressource
TO AI23A025;

-- Séquences = les serials (auto-increment)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public
TO AI23A025;

GRANT USAGE ON TYPE enum_etat_exemplaire, enum_personnel, enum_statut_adherent, 
enum_oeuvre, enum_type_contri_oeuvre_musical, enum_type_contri_film
TO AI23A025;
