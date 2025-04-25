# Schéma de Base de Données NurAI

## Introduction

NurAI utilise PostgreSQL comme système de gestion de base de données relationnelle. Ce document décrit la structure des tables, les relations entre elles et les types de données utilisés.

## Aperçu du Schéma

La base de données NurAI est organisée autour de plusieurs tables principales liées à un utilisateur central :

- **Users** : Informations d'authentification et profils utilisateurs
- **HealthSurveys** : Suivi de la santé générale et des signes vitaux
- **MentalWellness** : Suivi du bien-être mental et de l'humeur
- **TherapySessions** : Enregistrement des séances de thérapie
- **FitnessMetrics** : Suivi de l'activité physique et des entraînements
- **WorkoutPlans** : Plans d'entraînement personnalisés
- **PlannedWorkouts** : Entraînements planifiés dans un plan
- **Exercises** : Exercices individuels dans un entraînement planifié

## Diagramme Entité-Relation

```
┌───────────────┐
│     Users     │
├───────────────┤
│ id            │◄────────┐
│ username      │         │
│ email         │         │
│ password_hash │         │
│ ...           │         │
└───────┬───────┘         │
        │                 │
        │                 │
        │                 │
        │                 │
┌───────▼───────┐  ┌──────┴────────┐  ┌───────────────┐
│HealthSurveys  │  │MentalWellness │  │FitnessMetrics │
├───────────────┤  ├───────────────┤  ├───────────────┤
│ id            │  │ id            │  │ id            │
│ user_id       │  │ user_id       │  │ user_id       │
│ date          │  │ date          │  │ date          │
│ weight        │  │ mood_rating   │  │ steps         │
│ bp_systolic   │  │ anxiety_level │  │ distance      │
│ bp_diastolic  │  │ ...           │  │ ...           │
│ ...           │  └───────┬───────┘  └───────┬───────┘
└───────────────┘          │                  │
                           │                  │
                  ┌────────▼───────┐ ┌────────▼───────┐
                  │TherapySessions │ │  WorkoutPlans  │
                  ├───────────────┬┤ ├────────────────┤
                  │ id            │ │ id             │
                  │ user_id       │ │ user_id        │
                  │ date          │ │ name           │
                  │ therapist     │ │ description    │
                  │ ...           │ │ ...            │
                  └───────────────┘ └───────┬────────┘
                                            │
                                   ┌────────▼────────┐
                                   │ PlannedWorkouts │
                                   ├─────────────────┤
                                   │ id              │
                                   │ plan_id         │
                                   │ day_of_week     │
                                   │ workout_type    │
                                   │ ...             │
                                   └───────┬─────────┘
                                           │
                                  ┌────────▼────────┐
                                  │    Exercises    │
                                  ├─────────────────┤
                                  │ id              │
                                  │ workout_id      │
                                  │ name            │
                                  │ sets            │
                                  │ reps            │
                                  │ ...             │
                                  └─────────────────┘
```

## Description Détaillée des Tables

### Table : users

Stocke les informations d'authentification et les profils des utilisateurs.

| Colonne            | Type          | Contraintes                | Description                          |
|--------------------|---------------|----------------------------|--------------------------------------|
| id                 | Integer       | Primary Key, Auto-increment | Identifiant unique                   |
| username           | String(64)    | Unique, Index, Not Null    | Nom d'utilisateur                    |
| email              | String(120)   | Unique, Index, Not Null    | Adresse email                        |
| password_hash      | String(128)   | Not Null                   | Hash du mot de passe                 |
| first_name         | String(64)    |                            | Prénom                               |
| last_name          | String(64)    |                            | Nom de famille                       |
| date_of_birth      | Date          |                            | Date de naissance                    |
| gender             | String(20)    |                            | Genre                                |
| height             | Float         |                            | Taille en cm                         |
| weight             | Float         |                            | Poids en kg                          |
| language_preference| String(5)     | Default 'en'               | Préférence de langue                 |
| created_at         | DateTime      | Default CURRENT_TIMESTAMP  | Date de création du compte           |
| last_login         | DateTime      |                            | Dernière connexion                   |
| is_active          | Boolean       | Default TRUE               | Compte actif/inactif                 |
| is_admin           | Boolean       | Default FALSE              | Droits administrateur                |

### Table : health_surveys

Stocke les données de suivi de santé générale et des signes vitaux.

| Colonne                   | Type          | Contraintes                            | Description                          |
|---------------------------|---------------|----------------------------------------|--------------------------------------|
| id                        | Integer       | Primary Key, Auto-increment            | Identifiant unique                   |
| user_id                   | Integer       | Foreign Key (users.id), Not Null       | Référence à l'utilisateur            |
| date                      | Date          | Not Null, Default CURRENT_DATE         | Date de l'entrée                     |
| created_at                | DateTime      | Default CURRENT_TIMESTAMP              | Date de création de l'entrée         |
| weight                    | Float         |                                        | Poids en kg                          |
| blood_pressure_systolic   | Integer       |                                        | Pression artérielle systolique       |
| blood_pressure_diastolic  | Integer       |                                        | Pression artérielle diastolique      |
| heart_rate                | Integer       |                                        | Fréquence cardiaque (bpm)            |
| body_temperature          | Float         |                                        | Température corporelle (°C)          |
| sleep_duration            | Float         |                                        | Durée de sommeil (heures)            |
| sleep_quality             | Integer       |                                        | Qualité du sommeil (1-10)            |
| energy_level              | Integer       |                                        | Niveau d'énergie (1-10)              |
| stress_level              | Integer       |                                        | Niveau de stress (1-10)              |
| water_intake              | Float         |                                        | Consommation d'eau (litres)          |
| meal_quality              | Integer       |                                        | Qualité des repas (1-10)             |
| alcohol_consumption       | Boolean       |                                        | Consommation d'alcool (oui/non)      |
| smoking                   | Boolean       |                                        | Tabagisme (oui/non)                  |
| symptoms                  | Text          |                                        | Description des symptômes            |
| notes                     | Text          |                                        | Notes supplémentaires                |

### Table : mental_wellness

Stocke les données de suivi du bien-être mental et de l'humeur.

| Colonne             | Type          | Contraintes                            | Description                            |
|---------------------|---------------|----------------------------------------|----------------------------------------|
| id                  | Integer       | Primary Key, Auto-increment            | Identifiant unique                     |
| user_id             | Integer       | Foreign Key (users.id), Not Null       | Référence à l'utilisateur              |
| date                | Date          | Not Null, Default CURRENT_DATE         | Date de l'entrée                       |
| created_at          | DateTime      | Default CURRENT_TIMESTAMP              | Date de création de l'entrée           |
| mood_rating         | Integer       |                                        | Évaluation de l'humeur (1-10)          |
| anxiety_level       | Integer       |                                        | Niveau d'anxiété (1-10)                |
| depression_level    | Integer       |                                        | Niveau de dépression (1-10)            |
| focus_clarity       | Integer       |                                        | Clarté mentale/concentration (1-10)    |
| motivation          | Integer       |                                        | Niveau de motivation (1-10)            |
| social_connection   | Integer       |                                        | Connexion sociale (1-10)               |
| meditation_minutes  | Integer       |                                        | Minutes de méditation                  |
| gratitude_practice  | Boolean       |                                        | Pratique de la gratitude (oui/non)     |
| therapy_session     | Boolean       |                                        | Séance de thérapie (oui/non)           |
| work_stress         | Boolean       |                                        | Stress lié au travail (oui/non)        |
| financial_stress    | Boolean       |                                        | Stress financier (oui/non)             |
| relationship_stress | Boolean       |                                        | Stress relationnel (oui/non)           |
| health_stress       | Boolean       |                                        | Stress lié à la santé (oui/non)        |
| triggers            | Text          |                                        | Déclencheurs/stresseurs                |
| coping_strategies   | Text          |                                        | Stratégies d'adaptation utilisées      |
| journal_entry       | Text          |                                        | Entrée de journal                      |

### Table : therapy_sessions

Stocke les informations sur les séances de thérapie.

| Colonne         | Type          | Contraintes                            | Description                           |
|-----------------|---------------|----------------------------------------|---------------------------------------|
| id              | Integer       | Primary Key, Auto-increment            | Identifiant unique                    |
| user_id         | Integer       | Foreign Key (users.id), Not Null       | Référence à l'utilisateur             |
| date            | DateTime      | Not Null                               | Date et heure de la séance            |
| therapist       | String(100)   |                                        | Nom du thérapeute                     |
| session_type    | String(50)    |                                        | Type de thérapie                      |
| notes           | Text          |                                        | Notes sur la séance                   |
| follow_up_date  | DateTime      |                                        | Date de la prochaine séance           |
| created_at      | DateTime      | Default CURRENT_TIMESTAMP              | Date d'enregistrement                 |

### Table : fitness_metrics

Stocke les données de suivi de l'activité physique.

| Colonne           | Type          | Contraintes                            | Description                           |
|-------------------|---------------|----------------------------------------|---------------------------------------|
| id                | Integer       | Primary Key, Auto-increment            | Identifiant unique                    |
| user_id           | Integer       | Foreign Key (users.id), Not Null       | Référence à l'utilisateur             |
| date              | Date          | Not Null, Default CURRENT_DATE         | Date de l'entrée                      |
| created_at        | DateTime      | Default CURRENT_TIMESTAMP              | Date de création de l'entrée          |
| steps             | Integer       |                                        | Nombre de pas                         |
| distance          | Float         |                                        | Distance parcourue (km)               |
| active_minutes    | Integer       |                                        | Minutes d'activité                    |
| calories_burned   | Integer       |                                        | Calories brûlées                      |
| workout_type      | String(50)    |                                        | Type d'entraînement                   |
| workout_duration  | Integer       |                                        | Durée de l'entraînement (minutes)     |
| workout_intensity | Integer       |                                        | Intensité de l'entraînement (1-10)    |
| heart_rate_avg    | Integer       |                                        | Fréquence cardiaque moyenne           |
| heart_rate_max    | Integer       |                                        | Fréquence cardiaque maximale          |
| recovery_score    | Integer       |                                        | Score de récupération (1-10)          |
| soreness_level    | Integer       |                                        | Niveau de courbatures (1-10)          |
| workout_notes     | Text          |                                        | Notes sur l'entraînement              |

### Table : workout_plans

Stocke les plans d'entraînement personnalisés.

| Colonne         | Type          | Contraintes                            | Description                           |
|-----------------|---------------|----------------------------------------|---------------------------------------|
| id              | Integer       | Primary Key, Auto-increment            | Identifiant unique                    |
| user_id         | Integer       | Foreign Key (users.id), Not Null       | Référence à l'utilisateur             |
| name            | String(100)   | Not Null                               | Nom du plan                           |
| description     | Text          |                                        | Description du plan                   |
| created_at      | DateTime      | Default CURRENT_TIMESTAMP              | Date de création                      |

### Table : planned_workouts

Stocke les entraînements planifiés dans un plan.

| Colonne         | Type          | Contraintes                                | Description                           |
|-----------------|---------------|-------------------------------------------|---------------------------------------|
| id              | Integer       | Primary Key, Auto-increment                | Identifiant unique                    |
| plan_id         | Integer       | Foreign Key (workout_plans.id), Not Null   | Référence au plan d'entraînement      |
| day_of_week     | Integer       |                                           | Jour de la semaine (0=Lundi, 6=Dimanche) |
| workout_type    | String(50)    |                                           | Type d'entraînement                   |
| duration        | Integer       |                                           | Durée prévue (minutes)                |
| description     | Text          |                                           | Description de l'entraînement        |

### Table : exercises

Stocke les exercices individuels dans un entraînement planifié.

| Colonne         | Type          | Contraintes                                  | Description                           |
|-----------------|---------------|---------------------------------------------|---------------------------------------|
| id              | Integer       | Primary Key, Auto-increment                  | Identifiant unique                    |
| workout_id      | Integer       | Foreign Key (planned_workouts.id), Not Null  | Référence à l'entraînement planifié   |
| name            | String(100)   | Not Null                                     | Nom de l'exercice                     |
| sets            | Integer       |                                             | Nombre de séries                      |
| reps            | Integer       |                                             | Nombre de répétitions                 |
| weight          | Float         |                                             | Poids utilisé (kg)                   |
| duration        | Integer       |                                             | Durée (secondes), pour exercices chronométrés |
| notes           | Text          |                                             | Notes supplémentaires                |

## Indexation

Les index suivants sont créés pour optimiser les performances des requêtes fréquentes :

1. Index sur `users.username` et `users.email` pour accélérer les recherches lors de l'authentification
2. Index sur `user_id` et `date` pour toutes les tables de suivi (health_surveys, mental_wellness, fitness_metrics)
3. Index sur `plan_id` pour la table planned_workouts
4. Index sur `workout_id` pour la table exercises

## Contraintes

Les contraintes suivantes sont appliquées pour maintenir l'intégrité des données :

1. **Clés primaires** sur toutes les tables avec auto-incrémentation
2. **Clés étrangères** pour assurer les relations correctes entre les tables
3. **Contraintes d'unicité** sur username et email dans la table users
4. **Contraintes NOT NULL** sur les champs requis
5. **Valeurs par défaut** pour les champs comme date, created_at, etc.

## Triggers et Fonctions

Plusieurs déclencheurs (triggers) et fonctions sont définis pour maintenir l'intégrité des données et automatiser certaines opérations :

1. Mise à jour automatique du champ `last_login` lors de la connexion d'un utilisateur
2. Calcul du BMI (IMC) basé sur la hauteur et le poids dans le profil utilisateur
3. Archivage automatique des anciennes entrées pour optimiser les performances

## Migration et Évolution

Le schéma de base de données est géré par Flask-Migrate (basé sur Alembic), ce qui permet :

1. La création initiale du schéma
2. Les migrations incrémentales lors des changements
3. Le retour en arrière (rollback) si nécessaire
4. Le suivi des versions du schéma

## Modèle de Données Logique

Les modèles SQLAlchemy fournissent une abstraction orientée objet de la base de données, permettant d'accéder aux données comme suit :

```python
# Exemple d'utilisation du modèle de données

# Récupérer un utilisateur
user = User.query.filter_by(username='johndoe').first()

# Récupérer les entrées d'humeur d'un utilisateur pour les 7 derniers jours
from datetime import datetime, timedelta
one_week_ago = datetime.now().date() - timedelta(days=7)
mood_entries = MentalWellness.query.filter_by(user_id=user.id).filter(MentalWellness.date >= one_week_ago).all()

# Créer une nouvelle entrée de santé
new_health_entry = HealthSurvey(
    user_id=user.id,
    weight=75.5,
    blood_pressure_systolic=120,
    blood_pressure_diastolic=80,
    sleep_duration=7.5,
    sleep_quality=8
)
db.session.add(new_health_entry)
db.session.commit()
```

## Sécurité des Données

Les mesures suivantes sont mises en place pour assurer la sécurité des données dans la base de données :

1. Les mots de passe sont hachés avec l'algorithme bcrypt via Werkzeug
2. Les requêtes utilisent des paramètres liés pour éviter les injections SQL
3. L'accès à la base de données est limité par un utilisateur dédié avec des privilèges minimaux
4. Les connections à la base de données utilisent TLS/SSL pour le chiffrement en transit
5. Les sauvegardes régulières sont chiffrées

## Considérations de Performance

Pour maintenir de bonnes performances avec une croissance du volume de données :

1. Les requêtes sont optimisées pour utiliser les index
2. Les relations sont chargées via lazy loading ou eager loading selon le contexte
3. La pagination est utilisée pour limiter le volume de données récupérées
4. Des vues matérialisées peuvent être créées pour les requêtes d'analyse complexes
5. Les données historiques peuvent être archivées dans des tables séparées