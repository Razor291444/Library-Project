La génération marche pas toujours sur Gitlab, mais il existe un site
pour générer des png à partir du code PlantUML : https://www.plantuml.com/plantuml/uml/


```plantuml

@startuml
skinparam groupInheritance 2


class Exemplaire {
code: INTEGER {key}
etat: Etat
}

class Ressource {
code: INTEGER {key}
titre: VARCHAR
date_apparition: DATE
genre: VARCHAR
editeur: VARCHAR
prix: FLOAT
code_classification: VARCHAR
}
enum Etat {
Neuf
Bon
Abime
Perdu
}
class Film {
langue: VARCHAR
duree: INTERVAL
synopsis: TEXT
}
class Livre {
ISBN: VARCHAR
resume: TEXT
langue: VARCHAR
}

class OeuvreMusicale {
duree: FLOAT
}



class Contributeur {
id: INTEGER {key}
nom: VARCHAR
prenom: VARCHAR
date_naissance: DATE
nationalite: VARCHAR
}

class ContributionFilm {
type: TypeContributionFilm NOT NULL
}

class AutheurLivre{
}

class ContributionOeuvreMusicale {
type: TypeContributionMusicale NOT NULL
}

class Utilisateur {
login: VARCHAR {key}
mot_de_passe: VARCHAR
nom: VARCHAR
prenom: VARCHAR
adresse: VARCHAR
email: VARCHAR
}

class Personnel {

}

class Adherent {
date_naissance: DATE
telephone: VARCHAR
status: Status
}

enum Status {
Actif
Supprime
Blacklist
}

enum TypeContributionMusicale {
Compositeur
Interprete
CompositeurInterprete
}

enum TypeContributionFilm {
Acteur
Realisateur
ActeurRealisateur
}
class Pret {
code: INTEGER {local key}
date_pret: DATE
duree: FLOAT
/date_rendu: DATE
}

class Sanction {
id: INTEGER {key}
debut: DATE
fin: DATE = NULL
}
Film "0..*" -- "0..*" Contributeur: Contribue
(Film, Contributeur) .. ContributionFilm

OeuvreMusicale "0..*" -- "0..*" Contributeur: Contribue
(OeuvreMusicale, Contributeur) .. ContributionOeuvreMusicale

Livre "0..*" -- "0..*" Contributeur: Ecrit
(Livre, Contributeur) .. AutheurLivre

Ressource *-- "0..*" Exemplaire: Possède

Ressource <|-- Livre
Ressource <|-- OeuvreMusicale
Ressource <|-- Film

Utilisateur <|-- Personnel
Utilisateur <|-- Adherent

Adherent "1" -- "0..*" Sanction: Subit
Exemplaire "0..*" -- "0..*" Adherent: Emprunte {(etat = NEUF ou BON) et limite de x prets simultané}
(Exemplaire, Adherent) .. Pret

@enduml
```