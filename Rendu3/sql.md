## Création de tables

```sql
CREATE OR REPLACE TABLE Ressource (
code INT AUTO_INCREMENT PRIMARY KEY,
titre VARCHAR(255),
date_apparition DATE,
genre VARCHAR(50),
editeur VARCHAR(100),
prix DECIMAL(10, 2),
code_classification INT,
type ENUM('Livre', 'OeuvreMusicale', 'Film') NOT NULL,
CHECK (type IS NOT NULL)
);

CREATE OR REPLACE TABLE Film (
code INT PRIMARY KEY,
langue VARCHAR(50),
duree INT,
synopsis TEXT,
FOREIGN KEY (code) REFERENCES Ressource(code)
);

CREATE OR REPLACE TABLE Livre (
code INT PRIMARY KEY,
ISBN VARCHAR(20),
resume TEXT,
langue VARCHAR(50),
FOREIGN KEY (code) REFERENCES Ressource(code)
);

CREATE OR REPLACE TABLE OeuvreMusicale (
code INT PRIMARY KEY,
duree INT,
FOREIGN KEY (code) REFERENCES Ressource(code)
);

CREATE OR REPLACE TABLE Exemplaire (
code INT AUTO_INCREMENT PRIMARY KEY,
ressource INT,
etat ENUM('Neuf', 'Bon', 'Abime', 'Perdu'),
FOREIGN KEY (ressource) REFERENCES Ressource(code) ON DELETE CASCADE,
CHECK (ressource IS NOT NULL)
);

CREATE OR REPLACE TABLE Utilisateur (
login VARCHAR(50) PRIMARY KEY,
mot_de_passe VARCHAR(255) NOT NULL,
nom VARCHAR(50),
prenom VARCHAR(50),
adresse VARCHAR(255),
email VARCHAR(100),
type ENUM('Adherent', 'Personnel') NOT NULL,
CHECK (mot_de_passe IS NOT NULL),
CHECK (type IS NOT NULL)
);

CREATE OR REPLACE TABLE Adherent (
login VARCHAR(50) PRIMARY KEY,
date_naissance DATE,
telephone VARCHAR(20),
status ENUM('Actif', 'Supprime', 'Blacklist'),
FOREIGN KEY (login) REFERENCES Utilisateur(login) ON DELETE CASCADE
);

CREATE OR REPLACE TABLE Sanction (
id INT AUTO_INCREMENT PRIMARY KEY,
adherent VARCHAR(50),
debut DATE NOT NULL,
fin DATE,
FOREIGN KEY (adherent) REFERENCES Adherent(login) ON DELETE CASCADE,
CHECK (debut IS NOT NULL)
);

CREATE OR REPLACE TABLE Pret (
code INT AUTO_INCREMENT PRIMARY KEY,
adherent VARCHAR(50),
exemplaire INT,
date_pret DATE NOT NULL,
duree INT,
date_rendu DATE,
FOREIGN KEY (adherent) REFERENCES Adherent(login) ON DELETE CASCADE,
FOREIGN KEY (exemplaire) REFERENCES Exemplaire(code) ON DELETE CASCADE,
CHECK (date_pret IS NOT NULL)
);

CREATE OR REPLACE TABLE Contributeur (
id INT AUTO_INCREMENT PRIMARY KEY,
nom VARCHAR(50),
prenom VARCHAR(50),
date_naissance DATE,
nationalite VARCHAR(50)
);

CREATE OR REPLACE TABLE ContributionOeuvreMusicale (
contributeur INT,
oeuvre_musicale INT,
type ENUM('Interprete', 'Compositeur', 'InterpreteCompositeur') NOT NULL,
PRIMARY KEY (contributeur, oeuvre_musicale),
FOREIGN KEY (contributeur) REFERENCES Contributeur(id) ON DELETE CASCADE,
FOREIGN KEY (oeuvre_musicale) REFERENCES OeuvreMusicale(code) ON DELETE CASCADE,
CHECK (type IS NOT NULL)
);

CREATE OR REPLACE TABLE ContributionFilm (
contributeur INT,
film INT,
type ENUM('Acteur', 'Realisateur', 'ActeurRealisateur') NOT NULL,
PRIMARY KEY (contributeur, film),
FOREIGN KEY (contributeur) REFERENCES Contributeur(id) ON DELETE CASCADE,
FOREIGN KEY (film) REFERENCES Film(code) ON DELETE CASCADE,
CHECK (type IS NOT NULL)
);

CREATE OR REPLACE TABLE ContributionLivre (
contributeur INT,
livre INT,
PRIMARY KEY (contributeur, livre),
FOREIGN KEY (contributeur) REFERENCES Contributeur(id) ON DELETE CASCADE,
FOREIGN KEY (livre) REFERENCES Livre(code) ON DELETE CASCADE
);
```