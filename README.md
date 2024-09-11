# Documentation du Projet de Plateforme Électorale

## 1. Description Fonctionnelle

La plateforme électorale est conçue pour gérer les élections du club de l'école. Elle permet aux étudiants de poser leur candidature pour différents postes et de voter pour les candidats de leur choix.

### Fonctionnalités principales :

1. **Gestion des candidatures** :
   - Les étudiants peuvent soumettre leur candidature pour un poste spécifique.
   - Vérification de l'éligibilité des candidats basée sur leur matricule.

2. **Système de vote** :
   - Les étudiants peuvent voter pour les candidats aux différents postes.
   - Limitation à un seul vote par poste et par étudiant.
   - Vérification de l'éligibilité des votants basée sur leur matricule.

3. **Sécurité** :
   - Utilisation du hachage des adresses IP pour prévenir les votes multiples.
   - Validation des matricules pour s'assurer que seuls les étudiants autorisés peuvent voter ou se présenter.

## 2. Architecture Technique

L'application est construite en utilisant le framework Flask en Python, avec une base de données SQLite pour le stockage des données.

### Composants principaux :

1. **app.py** : Point d'entrée de l'application Flask.
2. **config.py** : Configuration de l'application, y compris les postes disponibles et les matricules autorisés.
3. **models.py** : Définition des modèles de données (Candidature et Vote).
4. **routes.py** : Gestion des routes et de la logique de l'application.
5. **utils.py** : Fonctions utilitaires pour le hachage et la validation.

### Base de données :

- Utilisation de SQLAlchemy comme ORM.
- Deux tables principales : Candidature et Vote.

### Sécurité :

- Hachage des adresses IP pour le suivi des votes.
- Validation des matricules pour l'autorisation des candidatures et des votes.

## 3. Guide de Déploiement

1. Cloner le dépôt du projet.
2. Installer les dépendances : `pip install -r requirements.txt`
3. Configurer les variables d'environnement si nécessaire.
4. Initialiser la base de données : `flask db upgrade`
5. Lancer l'application : `python app.py`

## 4. Maintenance et Évolution

- Mettre à jour régulièrement la liste des matricules autorisés dans `config.py`.
- Effectuer des sauvegardes régulières de la base de données.
- Envisager l'ajout de fonctionnalités comme la visualisation des résultats ou la gestion des campagnes électorales.