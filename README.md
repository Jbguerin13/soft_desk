# SoftDesk : Projet d'école [OpenClassrooms](https://openclassrooms.com/fr) - Application web de gestion de projets et de tickets

SoftDesk est une API RESTful permettant de gérer des projets, des tickets (issues), et des commentaires associés. Les contributeurs et les auteurs des projets peuvent collaborer pour suivre les problèmes et améliorations de manière efficace.

## Installation et exécution

### Prérequis

- Python 3.9 ou version supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/Jbguerin13/soft_desk.git
   cd softdesk
   ```

2. **Créer un environnement virtuel** :
   Sous Windows :
   ```bash
   python -m venv env
   env\Scripts\activate
   ```
   Sous macOS/Linux :
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Appliquer les migrations de la base de données** :
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Lancer le serveur** :
   ```bash
   python manage.py runserver
   ```

---

## Fonctionnalités principales

### Gestion des utilisateurs
- **Inscription** : Créez un compte utilisateur avec username, email, mot de passe, etc.
- **Authentification JWT** : Connectez-vous pour obtenir un token d'accès et un token de rafraîchissement.

### Gestion des projets
- **Créer un projet** : Ajoutez un nouveau projet avec un titre, une description et un type (Backend, Frontend, etc.).
- **Gérer les contributeurs** : Ajoutez ou supprimez des contributeurs pour un projet.
- **Lister les projets** : Visualisez les projets accessibles (en tant qu'auteur ou contributeur).

### Gestion des tickets (Issues)
- **Créer un ticket** : Ajoutez une issue à un projet.
- **Lister les tickets** : Visualisez les tickets associés à un projet.

### Gestion des commentaires
- **Ajouter un commentaire** : Commentez un ticket existant.
- **Lister les commentaires** : Affichez les commentaires d'un ticket.

---


## Tests Postman

Voici les étapes pour tester l'application à l'aide de Postman ou tout autre outil de test et de développement d'API.

### 1. **Créer un utilisateur**

**Endpoint** :
```
POST /api/users/
```
**Body** :
```json
{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "S3cretPassword!",
    "age": 18,
    "can_be_contacted": true,
    "can_data_be_shared": false
}
```

### 2. **Obtenir un token JWT**

**Endpoint** :
```
POST /api/token/
```
**Body** :
```json
{
    "username": "testuser",
    "password": "S3cretPassword!"
}
```
**Response** :
```json
{
    "refresh": "<refresh_token>",
    "access": "<access_token>"
}
```

**Note** : Utilisez le token d'accès pour les requêtes suivantes en ajoutant un header :
```
Authorization: Bearer <access_token>
```

### 3. **Créer un projet**

**Endpoint** :
```
POST /api/projects/
```
**Body** :
```json
{
    "title": "Mon Projet",
    "description": "Description de mon projet",
    "type": "BACKEND"
}
```

### 4. **Ajouter un contributeur à un projet**

**Endpoint** :
```
POST /api/projects/<project_id>/contributors/
```
**Body** :
```json
{
    "user": <user_id>
}
```

### 5. **Lister les tickets d'un projet**

**Endpoint** :
```
GET /api/projects/<project_id>/issues/
```

### 6. **Créer un ticket (Issue)**

**Endpoint** :
```
POST /api/projects/<project_id>/issues/
```
**Body** :
```json
{
    "title": "Bug critique",
    "description": "Corriger un bug critique",
    "priority": "HIGH",
    "tag": "BUG",
    "status": "TODO",
    "assignee": <user_id>
}
```

### 7. **Ajouter un commentaire à un ticket**

**Endpoint** :
```
POST /api/projects/<project_id>/issues/<issue_id>/comments/
```
**Body** :
```json
{
    "description": "Voici un commentaire pertinent."
}
```

### 8. **Lister les commentaires d'un ticket**

**Endpoint** :
```
GET /api/projects/<project_id>/issues/<issue_id>/comments/
```

### 9. **Supprimer une ressource (Projet, Issue ou Comment)**

**Endpoint pour supprimer un projet** :
```
DELETE /api/projects/<project_id>/
```

**Endpoint pour supprimer une issue** :
```
DELETE /api/projects/<project_id>/issues/<issue_id>/
```

**Endpoint pour supprimer un commentaire** :
```
DELETE /api/projects/<project_id>/issues/<issue_id>/comments/<comment_id>/
```

---
