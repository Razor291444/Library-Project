Nous avons décidé de garder un héritage par référence pour la Ressource car en passant par des classes filles, il aurait fallu créer 3 tables d’emprunt différentes et 3 tables de prêt différentes. En passant par une classe mère, il y aurait eu beaucoup d'attributs null dans Ressource.

Pour l'héritage Utilisateur, on décide également de passer par référence, avec la table Personnel qui n'a pas besoin d'être créée car le type dans Utilisateur suffit.
En passant par classe mere on aurait eu le meme probleme qu'avant avec des attribut venant d'Adherent null, et par classe fille nous n'avont pas la necessiter de recree 2 table avec presque les memes données.