CREATE VIEW VuePretsEnCours AS
SELECT
    P.code AS pret_code,
    U.login AS adherent_login,
    R.titre AS ressource_titre,
    P.date_pret,
    P.duree,
    P.date_rendu
FROM
    Pret P
JOIN
    Utilisateur U ON P.adherent = U.login
JOIN
    Exemplaire E ON P.exemplaire = E.code
JOIN
    Ressource R ON E.ressource = R.code
WHERE
    P.date_rendu IS NULL;

CREATE VIEW VueAdherentsStatut AS
SELECT
    U.login AS adherent_login,
    U.nom AS adherent_nom,
    U.prenom AS adherent_prenom,
    U.adresse,
    U.email,
    A.date_naissance,
    A.telephone,
    A.status AS adherent_statut
FROM
    Utilisateur U
JOIN
    Adherent A ON U.login = A.login;


