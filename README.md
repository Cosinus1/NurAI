# NurAI - Application de Suivi de Bien-être Mental, Physique et Santé Globale

NurAI est une application web complète de suivi de santé avec support pour le bien-être mental, la forme physique et les métriques de santé générale.

## Fonctionnalités

- Inscription et authentification des utilisateurs
- Questionnaire de santé complet
- Tableau de bord avec plusieurs modules de santé
- Suivi du bien-être mental
- Suivi de la condition physique
- Métriques de santé générale
- Support multilingue (anglais/français)
- Base de données PostgreSQL pour le stockage des données
- Configurations de déploiement Docker et Kubernetes

## Pour Commencer

### Prérequis

- Python 3.9+ avec pip
- Docker et Docker Compose
- Kubernetes (optionnel, pour le déploiement)
- PostgreSQL (géré par Docker)

### Installation

1. Cloner le dépôt
   ```
   git clone https://github.com/votre-nom/nurai.git
   cd nurai
   ```

2. Créer et activer un environnement virtuel
   ```
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. Installer les dépendances
   ```
   pip install -r requirements.txt
   ```

4. Configurer les variables d'environnement
   ```
   cp .env.example .env
   # Modifiez les valeurs dans .env selon vos besoins
   ```

5. Initialiser la base de données
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Exécuter l'application
   ```
   flask run
   ```

### Utilisation avec Docker

1. Construire et démarrer les conteneurs
   ```
   docker-compose up -d
   ```

2. Initialiser la base de données
   ```
   docker-compose exec web flask db init
   docker-compose exec web flask db migrate -m "Initial migration"
   docker-compose exec web flask db upgrade
   ```

3. Accéder à l'application à l'adresse http://localhost:5000

## Changement de Langue

NurAI prend en charge les langues anglaise et française. Vous pouvez changer de langue en utilisant le menu déroulant dans la barre de navigation supérieure. Votre préférence linguistique sera mémorisée pour les visites futures.

## Schéma de Base de Données

NurAI utilise PostgreSQL pour stocker les données utilisateur et les métriques de santé :

- Users: Informations d'authentification et de profil
- Surveys: Métriques de santé collectées à partir des questionnaires utilisateur
- mental_wellness: Métriques de bien-être mental
- fitness_metrics: Données de suivi de condition physique
- therapy_sessions: Informations sur les séances de thérapie
- workout_plans: Plans d'entraînement personnalisés

## Déploiement

L'application est développée localement sur Linux et sera déployée sur une instance Google Cloud via l'intégration continue/déploiement continu GitHub (CI/CD).

### Déploiement sur Google Kubernetes Engine (GKE)

1. Créer un projet dans Google Cloud
2. Activer les API : Container Registry, Kubernetes Engine, et Cloud Build
3. Créer un cluster Kubernetes
4. Configurer les secrets GitHub pour le CI/CD
5. Pousser vers la branche principale pour déclencher le déploiement

## Structure du Projet

```
nurai/
├── app/               # Code principal de l'application
│   ├── auth/          # Module d'authentification
│   ├── core/          # Fonctionnalités de base
│   ├── health/        # Module de suivi de santé
│   ├── mental/        # Module de bien-être mental
│   ├── fitness/       # Module de condition physique
│   ├── static/        # Fichiers statiques (CSS, JS)
│   ├── templates/     # Templates HTML
│   ├── translations/  # Fichiers de traduction
│   └── utils/         # Utilitaires et helpers
├── docs/              # Documentation
├── tests/             # Tests
├── kubernetes/        # Configurations Kubernetes
├── .github/           # Workflows GitHub Actions
├── config.py          # Configuration de l'application
├── docker-compose.yml # Configuration Docker Compose
├── Dockerfile         # Configuration Docker
└── run.py             # Point d'entrée de l'application
```

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'informations.