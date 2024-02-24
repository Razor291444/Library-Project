-- Minors changes to the database

-- We can drop the view VuePretsEnCours
-- because it's not needed by other views
DROP VIEW vuepretsencours;

CREATE VIEW VuePretsEnCours AS
SELECT
    P.code AS pret_code,
    U.login AS adherent_login,
    R.titre AS ressource_titre,
    E.code AS code_exemplaire,
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
    P.date_rendu > CURRENT_DATE;


-- For the web application, we need to add a new table
CREATE TABLE RessourceImage (
    ressource INTEGER NOT NULL REFERENCES Ressource(code),
    imageUrl VARCHAR(255) NOT NULL
);

-- Populate the table
INSERT INTO RessourceImage(ressource, imageUrl) VALUES
    (1, 'https://cdn1.booknode.com/book_cover/3551/full/le-petit-prince-3550683.jpg'),
    (2, 'https://m.media-amazon.com/images/I/91b3Xtjt0IL.jpg'),
    (3, 'https://miro.medium.com/v2/resize:fit:7084/1*6QXManBm7wsBgDiagqPH8Q.png'),
    (4, 'https://miro.medium.com/v2/resize:fit:7084/1*6QXManBm7wsBgDiagqPH8Q.png'),
    (5, 'https://ih1.redbubble.net/image.3672950723.5070/flat,750x,075,f-pad,750x1000,f8f8f8.jpg');


-- Inserts new resources
INSERT INTO Ressource (titre, date_apparition, genre, editeur, prix, code_classification, type)
VALUES ('Harry Potter   ', '1997-06-26', 'Fantasy', 'Bloomsbury Publishing', 11.99, 2, 'Livre'),
       ('Introduction to Algorithms', '1990-07-26', 'Informatique', 'MIT Press', 29.99, 2, 'Livre'),
       ('Clean Code', '2008-08-01', 'Informatique', 'Prentice Hall', 24.99, 2, 'Livre'),
       ('Joker', '2019-08-31', 'Drame', 'Warner Bros. Pictures', 19.99, 1, 'Film'),
       ('Oppenheimer', '2023-12-31', 'Biographie', 'Paramount Pictures', 24.99, 1, 'Film');

INSERT INTO Livre (code, ISBN, resume, langue)
VALUES (6, '978-0-7475-3269-6', 'Le premier livre de la célèbre série de J.K. Rowling.', 'Anglais'),
       (7, '978-0-262-03384-8', 'Un livre classique sur les algorithmes.', 'Anglais'),
       (8, '978-0-13-235088-4', 'Un guide essentiel pour écrire un code propre.', 'Anglais');

INSERT INTO Film (code, langue, duree, synopsis)
VALUES (9, 'Anglais', 122, 'Un film de crime psychologique mettant en vedette le personnage du Joker.'),
       (10, 'Anglais', 150, 'Un film biographique sur J. Robert Oppenheimer, le père de la bombe atomique.');

INSERT INTO RessourceImage (ressource, imageUrl) VALUES
    (6, 'https://static.posters.cz/image/750/harry-potter-philosopher-s-stone-i104639.jpg') ,
    (7, 'https://m.media-amazon.com/images/I/61O6K0yPmzL._AC_UF1000,1000_QL80_.jpg'),
    (8, 'https://m.media-amazon.com/images/I/51E2055ZGUL._AC_UF1000,1000_QL80_.jpg'),
    (9, 'https://fr.web.img6.acsta.net/pictures/19/09/03/12/02/4765874.jpg'),
    (10, 'https://fr.web.img5.acsta.net/pictures/23/05/26/16/52/2793170.jpg');

INSERT INTO Exemplaire (ressource, etat)
VALUES
  (6, 'Neuf'),
  (6, 'Bon'),
  (6, 'Neuf'),
  (7, 'Neuf'),
  (7, 'Bon'),
  (8, 'Neuf'),
  (8, 'Bon'),
  (9, 'Neuf'),
  (9, 'Bon'),
  (9, 'Neuf'),
  (10, 'Neuf'),
  (10, 'Bon'),
  (10, 'Bon');

INSERT INTO Contributeur (nom, prenom, date_naissance, nationalite)
VALUES ('Christopher', 'Nolan', '1970-07-30', 'Américain'),
       ('Joanne', 'Rowling', '1965-07-31', 'Britannique'),
       ('Thomas', 'Cormen', '1956-05-19', 'Américain'),
       ('Robert C.', 'Martin', '1952-12-05', 'Américain'),
       ('Joaquin', 'Phoenix', '1974-10-28', 'Américain'),
       ('Robert', 'Oppenheimer', '1904-04-22', 'Américain');

-- Petit Prince
INSERT INTO ContributionLivre (contributeur, livre)
VALUES
    (1, 1),  -- Antoine de Saint-Exupéry
    (2, 1);  -- Ernest Hemingway

-- 1984
INSERT INTO ContributionLivre (contributeur, livre)
VALUES
    (5, 3);  -- George Orwell

-- Introduction to Algorithms
INSERT INTO ContributionLivre (contributeur, livre)
VALUES
    (10, 7);  -- Thomas H. Cormen

-- Clean Code
INSERT INTO ContributionLivre (contributeur, livre)
VALUES
    (11, 8);  -- Robert C. Martin

-- Never Gonna Give You Up
INSERT INTO ContributionOeuvreMusicale (contributeur, oeuvre_musicale, type)
VALUES
    (8, 5, 'Interprete');  -- Rick Astley

-- Harry Potter
INSERT INTO ContributionLivre (contributeur, livre)
VALUES
    (9, 6);  -- Joanne Rowling

-- Joker
INSERT INTO ContributionFilm (contributeur, film, type)
VALUES
    (10, 9, 'Acteur'),  -- Joaquin Phoenix
    (3, 9, 'Realisateur');  -- Christopher Nolan

-- Oppenheimer
INSERT INTO ContributionFilm (contributeur, film, type)
VALUES
    (13, 10, 'Acteur'),  -- Cillian Murphy
    (3, 12, 'Realisateur');  -- Christopher Nolan

-- Inception
INSERT INTO ContributionFilm (contributeur, film, type)
VALUES
    (3, 2, 'Réalisateur'),
    (4, 2, 'Acteur');

-- Compte de Monte Cristo
INSERT INTO Ressource (titre, date_apparition, genre, editeur, prix, code_classification, type)
VALUES ('Le Comte de Monte Cristo', '1844-08-28', 'Aventure', 'Penguin Classics', 19.99, 1, 'Livre');

INSERT INTO Contributeur (id, nom, prenom, date_naissance, nationalite)
VALUES (14, 'Dumas', 'Alexandre', '1802-07-24', 'Française');

INSERT INTO Livre (code, ISBN, resume, langue)
VALUES (11, '9782253004225', 'Résumé du livre "Le Comte de Monte-Cristo".', 'Français');

INSERT INTO ContributionLivre (contributeur, livre)
VALUES (14, 1);

INSERT INTO Exemplaire (ressource, etat)
VALUES (11, 'Neuf'), (11, 'Bon');

INSERT INTO RessourceImage (ressource, imageUrl) VALUES
    (11, 'https://images.epagine.fr/647/9782072895647_1_75.jpg');

