## MLD

Ressource(#code, titre, date_apparition, genre, editeur, prix, code_classification, type) avec type non null

Film(#code => Ressource, langue, duree, synopsis)
Livre(#code=> Ressource, ISBN, resume, langue)
OeuvreMusicale(#code=> Ressource, duree)

Exemplaire(#code, ressource => Ressource, etat:[Neuf, Bin, Abime, Perdu]) avec ressource non null

Utilisateur(#login, mot_de_passe, nom, prenom, adresse, email, type) avec mot_de_passe, type non null

Adherent(#login => Utilisateur, date_naissance, telephone, status:[Actif, Supprime, Blacklist])

Sanction(#id,adherent=> Adherent, debut, fin) avec debut non null

Pret(#adherent=> Adherent, #exemplaire=> Exemplaire, #code, date_pret, duree, date_rendu) avec code clé local, début non null

Contributeur(#id, nom, prenom, date_naissance, nationalite)

ContributionOeuvreMusicale(#contributeur=>Contributeur, oeuvre_musicale => OeuvreMusicale, type:[Interprete, Compositeur, InterpreteCompositeur]) avec type non null

ContributionFilm(#contributeur=>Contributeur, #film=> Film, type:[Acteur, Réalisateur, ActeurRealisateur]) avec type non null

ContributionLivre(#contributeur=>Contributeur, #livre=> Livre)

## Vues

```sql
CREATE VIEW LivreView AS
SELECT
    l.code AS livre_code,
    r.titre,
    r.date_apparition,
    r.genre,
    r.editeur,
    r.prix,
    r.code_classification,
    r.type,
    l.ISBN,
    l.resume,
    l.langue,
    e.etat
FROM Livre l
JOIN Ressource r ON l.code = r.code;

CREATE VIEW FilmView AS
SELECT
    f.code AS film_code,
    r.titre,
    r.date_apparition,
    r.genre,
    r.editeur,
    r.prix,
    r.code_classification,
    r.type,
    f.langue,
    f.duree,
    f.synopsis,
    e.etat
FROM Film f
JOIN Ressource r ON f.code = r.code;


CREATE VIEW OeuvreMusicaleView AS
SELECT
    o.code AS oeuvre_musicale_code,
    r.titre,
    r.date_apparition,
    r.genre,
    r.editeur,
    r.prix,
    r.code_classification,
    r.type,
    o.duree,
    e.etat
FROM OeuvreMusicale o
JOIN Ressource r ON o.code = r.code;
```

## DFE et normalisation

Ressource : code -> titre, date_apparition, genre, editeur, prix, code_classification, type 

Film : code -> langue, duree, synopsis

Livre :code -> ISBN, resume, langue

OeuvreMusicale : code -> duree

Exemplaire : code -> ressource, etat

Utilisateur : login -> mot_de_passe, nom, prenom, adresse, email, type 

Adherent : login -> date_naissance, telephone, status

Sanction : id -> debut, fin, login

Pret : (adherent, exemplaire, code) -> date_pret, duree, date_rendu

Contributeur : id -> nom, prenom, date_naissance, nationalite

ContributionOeuvreMusicale : (contributeur, oeuvre_musicale) -> type

ContributionFilm : (contributeur, film=) -> type

ContributionLivre : Ø
