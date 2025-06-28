# Application d'Analyse Médicale Flask

Application Flask pour l'analyse d'images médicales avec détection d'objets.

## Déploiement sur Railway.com

### Étapes de déploiement :

1. **Préparer l'application localement**
   ```bash
   # Tester l'application avant déploiement
   ./test-local.sh
   
   # Remplacer requirements.txt par la version optimisée Railway
   mv requirements.txt requirements-dev.txt
   mv requirements-railway.txt requirements.txt
   ```

2. **Créer un compte sur Railway.com**
   - Allez sur https://railway.app/
   - Connectez-vous avec GitHub

3. **Préparer votre repository GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Railway deployment"
   git remote add origin <votre-repo-github>
   git push -u origin main
   ```

4. **Déployer sur Railway**
   - Cliquez sur "New Project"
   - Sélectionnez "Deploy from GitHub repo"
   - Choisissez votre repository
   - Railway détectera automatiquement que c'est une app Python

5. **Configuration des variables d'environnement**
   Dans les settings de votre projet Railway, ajoutez :
   ```
   SECRET_KEY=votre_cle_secrete_super_secure_changez_moi
   RAILWAY_ENVIRONMENT=production
   FLASK_ENV=production
   CONFIDENCE_THRESHOLD=0.4
   MODEL_PATH=best.pt
   ```

6. **Optionnel: Ajouter PostgreSQL**
   - Dans Railway, cliquez sur "Add service" > "Database" > "PostgreSQL"
   - Railway configurera automatiquement DATABASE_URL

### Fichiers de configuration créés :

- `Procfile` : Spécifie comment démarrer l'application
- `runtime.txt` : Version Python à utiliser  
- `railway.toml` : Configuration Railway
- `start.sh` : Script de démarrage optimisé
- `test-local.sh` : Script de test avant déploiement
- `.railwayignore` : Fichiers à ignorer lors du déploiement
- `requirements-railway.txt` : Dépendances optimisées pour Railway
- `config.py` : Configuration centralisée pour différents environnements
- `.env.example` : Exemple de variables d'environnement

### Points importants :

1. **Modèles YOLO** : Assurez-vous que `best.pt` et/ou `best1.pt` sont dans le repository
2. **Base de données** : En production, Railway peut fournir PostgreSQL automatiquement
3. **Stockage des fichiers** : Les fichiers uploadés ne persistent pas sur Railway. Considérez :
   - AWS S3
   - Cloudinary  
   - Railway Volumes (pour stockage persistant)
4. **Variables d'environnement** : Toujours utiliser les variables d'environnement pour les informations sensibles
5. **Performance** : L'application est configurée pour une instance avec timeout étendu (300s) pour le traitement d'images

### Commandes utiles après déploiement :

```bash
# Voir les logs
railway logs

# Redéployer
git push origin main

# Variables d'environnement
railway variables set SECRET_KEY=nouvelle_cle
```

### Dépannage :

- Si l'application ne démarre pas, vérifiez les logs avec `railway logs`
- Assurez-vous que tous les fichiers nécessaires sont dans le repository
- Vérifiez que les variables d'environnement sont correctement configurées
