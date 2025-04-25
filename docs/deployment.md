# Guide de Déploiement NurAI

Ce document détaille le processus de déploiement de l'application NurAI, de l'environnement de développement local jusqu'à la production sur Google Cloud Platform avec Kubernetes.

## Table des matières

1. [Prérequis](#prérequis)
2. [Environnement de développement](#environnement-de-développement)
3. [Préparation pour la production](#préparation-pour-la-production)
4. [Déploiement sur Google Kubernetes Engine (GKE)](#déploiement-sur-google-kubernetes-engine-gke)
5. [Configuration CI/CD avec GitHub Actions](#configuration-cicd-avec-github-actions)
6. [Surveillance et maintenance](#surveillance-et-maintenance)
7. [Procédures de sauvegarde et restauration](#procédures-de-sauvegarde-et-restauration)
8. [Troubleshooting](#troubleshooting)

## Prérequis

Pour déployer NurAI, les éléments suivants sont nécessaires :

- Compte GitHub pour le code source
- Compte Google Cloud Platform avec facturation activée
- gcloud CLI installé et configuré
- kubectl installé
- Docker et Docker Compose installés (pour le développement local)

## Environnement de développement

### Installation et configuration

1. Cloner le dépôt
   ```bash
   git clone https://github.com/your-organization/nurai.git
   cd nurai
   ```

2. Créer le fichier .env à partir du template
   ```bash
   cp .env.example .env
   ```
   Modifier les variables selon vos besoins, notamment :
   - `SECRET_KEY` - Clé secrète pour l'application Flask
   - `DB_USER` - Utilisateur PostgreSQL
   - `DB_PASSWORD` - Mot de passe PostgreSQL

3. Démarrer l'environnement de développement avec Docker Compose
   ```bash
   docker-compose up -d
   ```

4. Initialiser la base de données
   ```bash
   docker-compose exec web flask db init
   docker-compose exec web flask db migrate -m "Initial migration"
   docker-compose exec web flask db upgrade
   ```

5. Accéder à l'application à l'adresse [http://localhost:5000](http://localhost:5000)

### Développement local

- Les modifications du code sont automatiquement détectées grâce au volume monté
- Redémarrer le conteneur en cas de changement des dépendances :
  ```bash
  docker-compose restart web
  ```

- Visualiser les logs de l'application :
  ```bash
  docker-compose logs -f web
  ```

## Préparation pour la production

### Construction de l'image Docker

1. Construire l'image
   ```bash
   docker build -t gcr.io/[PROJECT_ID]/nurai:latest .
   ```

2. Tester l'image localement
   ```bash
   docker run -p 8080:8080 --env-file .env.prod gcr.io/[PROJECT_ID]/nurai:latest
   ```

### Stockage des secrets

Avant le déploiement sur GKE, créez les secrets Kubernetes :

```bash
# Créer un fichier .env.prod avec les variables d'environnement de production
kubectl create secret generic nurai-secrets \
  --from-literal=secret-key=$(openssl rand -hex 32) \
  --from-literal=db-user=postgres \
  --from-literal=db-password=$(openssl rand -hex 16)
```

## Déploiement sur Google Kubernetes Engine (GKE)

### Configuration de GKE

1. Créer un projet Google Cloud (si ce n'est pas déjà fait)
   ```bash
   gcloud projects create [PROJECT_ID] --name="NurAI Application"
   gcloud config set project [PROJECT_ID]
   ```

2. Activer les APIs nécessaires
   ```bash
   gcloud services enable container.googleapis.com \
     containerregistry.googleapis.com \
     cloudbuild.googleapis.com
   ```

3. Créer un cluster Kubernetes
   ```bash
   gcloud container clusters create nurai-cluster \
     --zone us-central1-a \
     --num-nodes 2 \
     --machine-type e2-standard-2
   ```

4. Obtenir les identifiants pour kubectl
   ```bash
   gcloud container clusters get-credentials nurai-cluster --zone us-central1-a
   ```

### Déploiement manuel (sans CI/CD)

1. Pousser l'image Docker vers Google Container Registry
   ```bash
   docker push gcr.io/[PROJECT_ID]/nurai:latest
   ```

2. Appliquer les configurations Kubernetes
   ```bash
   kubectl apply -f kubernetes/persistent-volume.yaml
   kubectl apply -f kubernetes/deployment.yaml
   kubectl apply -f kubernetes/service.yaml
   kubectl apply -f kubernetes/ingress.yaml
   ```

3. Vérifier le déploiement
   ```bash
   kubectl get pods
   kubectl get services
   kubectl get ingress
   ```

## Configuration CI/CD avec GitHub Actions

### Préparation des identifiants pour GitHub Actions

1. Créer un compte de service Google Cloud
   ```bash
   gcloud iam service-accounts create github-actions
   ```

2. Attribuer les rôles nécessaires
   ```bash
   gcloud projects add-iam-policy-binding [PROJECT_ID] \
     --member=serviceAccount:github-actions@[PROJECT_ID].iam.gserviceaccount.com \
     --role=roles/container.developer

   gcloud projects add-iam-policy-binding [PROJECT_ID] \
     --member=serviceAccount:github-actions@[PROJECT_ID].iam.gserviceaccount.com \
     --role=roles/storage.admin
   ```

3. Créer la clé JSON pour le compte de service
   ```bash
   gcloud iam service-accounts keys create github-actions-key.json \
     --iam-account=github-actions@[PROJECT_ID].iam.gserviceaccount.com
   ```

4. Ajouter les secrets dans GitHub
   - Dans votre dépôt GitHub, allez dans Settings > Secrets > Actions
   - Ajoutez deux secrets :
     - `GCP_PROJECT_ID` : Votre ID de projet Google Cloud
     - `GCP_SA_KEY` : Contenu du fichier github-actions-key.json

### Configuration du workflow GitHub Actions

Le workflow est déjà défini dans le fichier `.github/workflows/main.yml`. Il effectue les actions suivantes :

1. Checkout du code source
2. Configuration de l'environnement Google Cloud
3. Construction de l'image Docker
4. Push de l'image vers Google Container Registry
5. Déploiement sur GKE

### Déclenchement du déploiement

Le déploiement est automatiquement déclenché lorsqu'un push est effectué sur la branche main :

```bash
git add .
git commit -m "Ready for production"
git push origin main
```

## Surveillance et maintenance

### Surveillance

1. Configurer Cloud Monitoring
   ```bash
   gcloud services enable monitoring.googleapis.com
   ```

2. Accéder au tableau de bord de surveillance dans GCP Console
   - Allez à [https://console.cloud.google.com/monitoring](https://console.cloud.google.com/monitoring)
   - Créez des tableaux de bord pour surveiller :
     - Charge CPU et mémoire des pods
     - Latence des requêtes
     - Taux d'erreur
     - Trafic réseau

3. Configurer des alertes
   ```bash
   # Exemple avec gcloud (vous pouvez aussi le faire dans la console)
   gcloud alpha monitoring policies create \
     --display-name="High CPU Usage Alert" \
     --conditions="condition: metric.type=\"kubernetes.io/container/cpu/utilization\" resource.type=\"k8s_container\" comparison.gt_comparison.threshold_value=0.8"
   ```

### Mise à l'échelle

Configurez l'autoscaling horizontal pour ajuster le nombre de pods en fonction de la charge :

```bash
kubectl autoscale deployment nurai-web --min=2 --max=10 --cpu-percent=70
```

## Procédures de sauvegarde et restauration

### Sauvegarde de la base de données

1. Planifier des sauvegardes régulières
   ```bash
   # Créer un CronJob Kubernetes pour la sauvegarde
   kubectl apply -f kubernetes/backup-cronjob.yaml
   ```

2. Sauvegarde manuelle
   ```bash
   kubectl exec -it $(kubectl get pods -l app=nurai,tier=db -o jsonpath='{.items[0].metadata.name}') -- \
     pg_dump -U postgres nurai > backup_$(date +%Y%m%d_%H%M%S).sql
   ```

### Restauration

1. Copier le fichier de sauvegarde dans le pod
   ```bash
   kubectl cp backup_20250425_120000.sql \
     $(kubectl get pods -l app=nurai,tier=db -o jsonpath='{.items[0].metadata.name}'):/tmp/
   ```

2. Restaurer la base de données
   ```bash
   kubectl exec -it $(kubectl get pods -l app=nurai,tier=db -o jsonpath='{.items[0].metadata.name}') -- \
     psql -U postgres -d nurai -f /tmp/backup_20250425_120000.sql
   ```

## Troubleshooting

### Problèmes courants et solutions

1. **Les pods ne démarrent pas**
   ```bash
   # Vérifier l'état des pods
   kubectl get pods
   
   # Consulter les logs
   kubectl logs [POD_NAME]
   
   # Décrire le pod pour plus de détails
   kubectl describe pod [POD_NAME]
   ```

2. **Erreurs de base de données**
   ```bash
   # Vérifier que le pod PostgreSQL est en cours d'exécution
   kubectl get pods -l app=nurai,tier=db
   
   # Vérifier les logs
   kubectl logs $(kubectl get pods -l app=nurai,tier=db -o jsonpath='{.items[0].metadata.name}')
   
   # Se connecter à PostgreSQL pour vérifier manuellement
   kubectl exec -it $(kubectl get pods -l app=nurai,tier=db -o jsonpath='{.items[0].metadata.name}') -- \
     psql -U postgres
   ```

3. **L'application n'est pas accessible**
   ```bash
   # Vérifier l'état de l'ingress
   kubectl get ingress
   
   # Vérifier l'état du service
   kubectl get service nurai-service
   
   # Effectuer un port-forward pour tester directement
   kubectl port-forward service/nurai-service 8080:80
   ```

### Récupération en cas de panne

Si l'application rencontre des problèmes graves, vous pouvez effectuer un rollback à une version précédente :

```bash
# Rollback du déploiement à la révision précédente
kubectl rollout undo deployment/nurai-web

# Ou spécifier une révision spécifique
kubectl rollout undo deployment/nurai-web --to-revision=2
```

## Migration vers une nouvelle version

1. Mettre à jour le code sur la branche principale
2. Laisser le workflow CI/CD effectuer le déploiement
3. Vérifier que la mise à jour s'est bien déroulée
   ```bash
   kubectl get pods  # Vérifier que les pods sont en cours d'exécution
   kubectl logs -l app=nurai,tier=web  # Vérifier les logs
   ```