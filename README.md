exemples de tests à effectuer

**Créer un nouvel utilisateur**

Méthode : POST
URL : http://127.0.0.1:8000/api/users/

Méthode : GET
URL : http://127.0.0.1:8000/api/users/

exemple Body JSON :

{
    "username": "john_doe",
    "email": "john@example.com",
    "age": 25,
    "can_be_contacted": true,
    "can_data_be_shared": false
}



**modifier un utilisateur**

Méthode : PUT
URL : http://127.0.0.1:8000/api/users/1/
même body


**acceder aux utilisateurs enregistrés en base**

Méthode : GET
URL : http://127.0.0.1:8000/users/



**supprimer un utilisateur**

Méthode : DELETE
URL : http://127.0.0.1:8000/api/users/1/