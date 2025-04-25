# Architecture de l'Application NurAI

## Vue d'ensemble

NurAI est une application web développée avec Flask qui permet aux utilisateurs de suivre leur bien-être mental, leur condition physique et leur santé générale. L'application suit une architecture modulaire basée sur des blueprints Flask et utilise une base de données PostgreSQL pour le stockage des données.

## Architecture Technique

### Structure de l'Application

L'application suit le modèle MVC (Modèle-Vue-Contrôleur) et est organisée selon une architecture modulaire :

- **Modèles** : Définissent la structure des données et les relations entre elles
- **Vues** : Templates HTML avec Jinja2 pour le rendu des pages
- **Contrôleurs** : Routes Flask qui traitent les requêtes et renvoient les réponses

### Composants Principaux

1. **Core** : Module principal de l'application, gère la page d'accueil et le tableau de bord
2. **Auth** : Gestion de l'authentification et des profils utilisateurs
3. **Health** : Suivi des métriques de santé générale
4. **Mental** : Suivi du bien-être mental et des journaux d'humeur
5. **Fitness** : Suivi de l'activité physique et des plans d'entraînement

### Technologies Utilisées

- **Backend** : Python 3.9+ avec Flask 2.2+
- **Base de données** : PostgreSQL 13
- **ORM** : SQLAlchemy via Flask-SQLAlchemy
- **Frontend** : HTML5, CSS3, JavaScript
- **Framework CSS** : Bootstrap 5
- **Bibliothèque de graphiques** : Chart.js
- **Internationalisation** : Flask-Babel
- **Authentification** : Flask-Login
- **Formulaires** : Flask-WTF
- **Migrations de base de données** : Flask-Migrate (Alembic)

## Flux de Données

1. L'utilisateur envoie une requête HTTP à l'application
2. Le dispatcher de Flask achemine la requête vers la route appropriée
3. La fonction de la route (contrôleur) traite la requête :
   - Récupère/modifie les données via les modèles
   - Prépare les données pour l'affichage
4. Le template est rendu avec les données et renvoyé à l'utilisateur
5. Le navigateur affiche la page HTML résultante

## Diagramme d'Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Navigateur                           │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/HTTPS
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Serveur Web (Gunicorn)                 │
└───────────────────────────┬─────────────────────────────────┘
                            │ WSGI
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Application Flask                      │
│  ┌─────────┐  ┌──────────┐  ┌─────────┐  ┌──────────────┐   │
│  │   Auth  │  │   Core   │  │ Mental  │  │   Fitness    │   │
│  └────┬────┘  └─────┬────┘  └────┬────┘  └──────┬───────┘   │
│       │            │            │               │           │
│       └────────────┼────────────┼───────────────┘           │
│                    │            │                           │
│  ┌─────────────────▼────────────▼───────────────────────┐   │
│  │                  SQLAlchemy ORM                      │   │
│  └─────────────────────────┬─────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Base de données PostgreSQL             │
└─────────────────────────────────────────────────────────────┘
```

## Architecture de Déploiement

L'application est conçue pour être déployée dans un environnement conteneurisé avec Docker et orchestrée via Kubernetes.

### Environnement de Développement

- Conteneurs Docker via docker-compose
- Volume monté pour le développement en temps réel
- Base de données PostgreSQL dans un conteneur

### Environnement de Production

- Cluster Kubernetes sur Google Cloud Platform
- Déploiement via GitLab CI/CD
- Exposition via Ingress
- Stockage persistant pour la base de données PostgreSQL
- Mise à l'échelle automatique basée sur la charge

```
┌──────────────────────────────────────────────────┐
│                Google Kubernetes Engine           │
│                                                  │
│  ┌──────────────┐       ┌─────────────────────┐  │
│  │   Ingress    │──────►│  Service NurAI      │  │
│  └──────────────┘       └──────────┬──────────┘  │
│                                    │             │
│                                    ▼             │
│  ┌──────────────┐       ┌─────────────────────┐  │
│  │  Autoscaler  │◄─────►│ Pods NurAI (2+)     │  │
│  └──────────────┘       └──────────┬──────────┘  │
│                                    │             │
│                                    ▼             │
│  ┌──────────────┐       ┌─────────────────────┐  │
│  │  PostgreSQL  │◄─────►│  Service PostgreSQL │  │
│  │  Persistant  │       └─────────────────────┘  │
│  │  Volume      │                                │
│  └──────────────┘                                │
└──────────────────────────────────────────────────┘
```

## Sécurité

- Authentification basée sur Flask-Login
- Mots de passe hachés avec Werkzeug
- Protection CSRF via Flask-WTF
- En-têtes de sécurité HTTP
- Cookies sécurisés avec attributs HttpOnly et Secure
- Validation des entrées utilisateur
- Protection contre les injections SQL via SQLAlchemy

## Extensibilité

L'architecture modulaire permet d'ajouter facilement de nouveaux modules ou de modifier les modules existants. Pour ajouter une nouvelle fonctionnalité :

1. Créer un nouveau blueprint Flask
2. Définir les modèles nécessaires
3. Implémenter les routes
4. Créer les templates
5. Enregistrer le blueprint dans l'application principale

## Internationalisation

L'application prend en charge plusieurs langues via Flask-Babel. Pour ajouter une nouvelle langue :

1. Extraire les chaînes de caractères à traduire
2. Créer un nouveau fichier de traduction
3. Compiler les fichiers de traduction

## Performances

- Mise en cache côté client
- Pagination des résultats de requêtes
- Indexation de base de données
- Lazy loading des relations SQLAlchemy
- Compression gzip des réponses