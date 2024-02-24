# Note de clarification

### Contexte

Conception d'un système de gestion pour une bibliothèque municipale qui souhaite 
informatiser ses activités : catalogage, consultations, gestion des utilisateurs, prêts. 

Cela permet de :

* Faciliter aux adhérents la recherche de documents et la gestion de leurs emprunts.
* Faciliter la gestion des ressources documentaires : ajouter des documents, modifier leur description, ajouter des exemplaires d'un document.
* Faciliter au personnel la gestion des prêts, des retards et des réservation.
* Faciliter la gestion des utilisateurs et de leurs données.Établir des statistiques sur les documents empruntés par les adhérents, cela permettra par exemple d'établir la liste des documents populaires, mais aussi d'étudier le profil des adhérents pour pouvoir leur suggérer des documents.

### Solution apportée

Réalisation d'une application Python, connectée à une base de données SQL afin de gérer 
la bibliothèque municipale.

### Objets modélisés 

On utilisera largement la possibilité d'hériter d'une autre table,
permise par le SGBD PostgresSQL.

Nous sommes partis du principe qu'un utilisateur peut être soit un adhérent, soit du personnel. Dans le cas d'un adhérent :

- Son compte peut être soit actif, soit non actif. Cela permet, lors de la suppression d'un compte, de conserver l'historique. La variable "blacklist" permet également de bloquer un adhérent.
- Il peut avoir des sanctions avec une date de départ (date de l'infraction) :
     - Si c'est un retard, alors on met la date de fin = date début + retard.
     - Si c'est une dégradation, on ne met pas de date de fin (qui sera changée lors d'un remboursement).
- L'adhérent peut ainsi emprunter des livres. L'utilisation d'une local key permet d'emprunter le même livre plusieurs fois. Il ne peut emprunter que des exemplaires, donc des ressources disponibles.
- Nous avons ajouté un prix dans Ressource utilisable dans le cas d'une demande de remboursement en cas de dégradation.

Des classes d'associations ont été utilisées pour la liste des contributeurs par type de ressource, permettant une organisation plus simple. 
Cependant, il aurait probablement été plus judicieux de créer uniquement une classe d'association entre ressource et contributeur nommée "Contribution" avec un type de contribution (acteur, réalisateur, etc.).
(voir dossier proposition)

