
INSERT INTO Ressource (titre, date_apparition, genre, editeur, prix, code_classification, type)
VALUES
    ('Le Petit Prince', '1943-04-06', 'Fiction', 'Gallimard', 15.99, 1, 'Livre'),
    ('Inception', '2010-07-16', 'Science Fiction', 'Warner Bros.', 39.99, 3, 'Film'),
    ('1984', '1949-06-08', 'Dystopie', 'Secker & Warburg', 19.99, 1, 'Livre'),
    ('The Godfather', '1972-03-14', 'Crime', 'Paramount Pictures', 49.99, 3, 'Film'),
    ('Never Gonna Give You Up', '1987-07-27', 'Pop', 'RCA Records', 1.29, 2, 'OeuvreMusicale');

INSERT INTO Film (code, langue, duree, synopsis)
VALUES
    (2, 'Anglais', 150, 'Biopic sur le groupe Queen et Freddie Mercury.'),
    (4, 'Anglais', 170, 'Le Parrain : saga mafieuse de la famille Corleone.');

INSERT INTO Livre (code, ISBN, resume, langue)
VALUES
    (1, '9782070292959', 'Le Petit Prince est un conte philosophique.', 'Français'),
    (3, '9782072730030', 'Classique de la littérature américaine.', 'Anglais');

INSERT INTO OeuvreMusicale (code, duree)
VALUES (5, 213);

-- Le Petit Prince
INSERT INTO Exemplaire (ressource, etat) VALUES
    (1, 'Neuf'),
    (1, 'Bon');

-- Inception
INSERT INTO Exemplaire (ressource, etat) VALUES
    (2, 'Neuf'),
    (2, 'Bon');

-- 1984
INSERT INTO Exemplaire (ressource, etat) VALUES
    (3, 'Neuf'),
    (3, 'Bon');

-- The Godfather
INSERT INTO Exemplaire (ressource, etat) VALUES
    (4, 'Neuf'),
    (4, 'Bon');

-- Exemplaires pour Never Gonna Give You Up
INSERT INTO Exemplaire (ressource, etat) VALUES
    (5, 'Neuf'),
    (5, 'Bon');

INSERT INTO Utilisateur (login, mot_de_passe, nom, prenom, adresse, email, type) VALUES
    ('amartin', '1234', 'Alice', 'Martin', '123 Rue des Roses', 'alice@example.com', 'Adherent'),
    ('bjohnson', '5678', 'Bob', 'Johnson', '456 Avenue des Arbres', 'bob@example.com', 'Personnel'),
    ('csmith', '9012', 'Charlie', 'Smith', '789 Chemin des Montagnes', 'charlie@example.com', 'Administrateur');

INSERT INTO Adherent (login, date_naissance, telephone, status) VALUES
    ('amartin', '1990-05-15', '123456789', 'Actif'),
    ('bjohnson', '1982-08-20', '987654321', 'Actif'),
    ('csmith', '1995-02-01', '555555555', 'Actif');

INSERT INTO Sanction (adherent, debut, fin) VALUES ('amartin', '2023-07-10', '2023-08-10');

INSERT INTO Pret (adherent, exemplaire, date_pret, duree, date_rendu) VALUES
    ('amartin', 1, '2023-12-01', 14, '2023-12-15'),
    ('csmith', 5, '2023-12-01', 21, '2023-12-22'),
    ('bjohnson', 10, '2023-12-01', 7, '2023-12-08');

-- Petit Prince
INSERT INTO Contributeur (nom, prenom, date_naissance, nationalite) VALUES
    ('Saint-Exupéry', 'Antoine', '1900-06-29', 'Française'),
    ('Hemingway', 'Ernest', '1899-07-21', 'Américaine');

-- Inception
INSERT INTO Contributeur (nom, prenom, date_naissance, nationalite) VALUES
    ('Nolan', 'Christopher', '1970-07-30', 'Britannique'),
    ('DiCaprio', 'Leonardo', '1974-11-11', 'Américaine');

-- 1984
INSERT INTO Contributeur (nom, prenom, date_naissance, nationalite) VALUES ('Orwell', 'George', '1903-06-25', 'Britannique');

-- The Godfather
INSERT INTO Contributeur (nom, prenom, date_naissance, nationalite) VALUES
    ('Coppola', 'Francis Ford', '1939-04-07', 'Américaine'),
    ('Brando', 'Marlon', '1924-04-03', 'Américaine');

-- Never Gonna Give You Up
INSERT INTO Contributeur (nom, prenom, date_naissance, nationalite) VALUES ('Astley', 'Rick', '1966-02-06', 'Britannique');

INSERT INTO ContributionLivre (contributeur, livre)
VALUES
    (1, 1), -- Antoine de Saint-Exupéry
    (2, 1); -- Ernest Hemingway

INSERT INTO ContributionFilm (contributeur, film, type)
VALUES
    (3, 2, 'Realisateur'), -- Christopher Nolan
    (4, 2, 'Acteur');      -- Leonardo DiCaprio

INSERT INTO ContributionLivre (contributeur, livre)
VALUES (4, 3); -- George Orwell

INSERT INTO ContributionFilm (contributeur, film, type)
VALUES
    (6, 4, 'Realisateur'), -- Francis Ford Coppola
    (7, 4, 'Acteur');      -- Marlon Brando

INSERT INTO ContributionOeuvreMusicale (contributeur, oeuvre_musicale, type)
VALUES
    (8, 5, 'Interprete'); -- Rick Astley
    