# Application d'Analyse Médicale Flask

Application Flask pour l'analyse d'images médicales avec détection d'objets utilisant YOLO.

## 🚀 Déploiement Rapide sur Railway.com

### Option 1: Script automatique (Recommandé)

```bash
./deploy-railway.sh
```

Ce script vérifie automatiquement:
- ✅ Présence des fichiers critiques
- ✅ Modèles YOLO (best.pt, best1.pt) - **6.5MB chacun**
- ✅ Configuration Git
- ✅ Optimisation des dépendances

### Option 2: Déploiement manuel

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
   SECRET_KEY=votre_cle_secrete_super_secure
   RAILWAY_ENVIRONMENT=production
   CONFIDENCE_THRESHOLD=0.4
   ```

## 📋 Architecture du Projet

```
├── app.py                 # Application Flask principale
├── config.py              # Configuration environnements
├── model_config.py        # Configuration modèles YOLO
├── routes.py              # Routes de l'application
├── models.py              # Modèles SQLAlchemy
├── forms.py               # Formulaires WTF
├── best.pt, best1.pt      # Modèles YOLO (6.5MB chacun)
├── Procfile               # Configuration Railway
├── runtime.txt            # Version Python
├── railway.toml           # Configuration Railway
├── requirements.txt       # Dépendances Python
└── deploy-railway.sh      # Script de déploiement
```

## 🔧 Fichiers de Configuration Railway

### Créés automatiquement:

- **`Procfile`** : `web: gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 300 app:app`
- **`runtime.txt`** : `python-3.12.0`
- **`railway.toml`** : Configuration Railway
- **`model_config.py`** : Gestion des modèles YOLO
- **`init.sh`** : Script d'initialisation
- **`.railwayignore`** : Fichiers à ignorer

### Optimisations pour Railway:

1. **Dépendances allégées** : CPU-only versions (torch, opencv-headless)
2. **Gestion mémoire** : 1 worker, timeout 300s
3. **Healthcheck** : Endpoint `/health` pour monitoring
4. **Configuration adaptative** : Auto-détection environnement Railway

## 🎯 Points Critiques pour Railway

### ✅ Avantages de votre configuration:
- **Modèles légers**: 6.5MB chacun (✓ Compatible Railway)
- **Base SQLite**: Parfait pour démarrer
- **Configuration flexible**: Support dev/prod
- **Healthcheck intégré**: Monitoring automatique

### ⚠️ Limitations Railway à considérer:

1. **Stockage éphémère**: Les fichiers uploadés ne persistent pas
   - **Solution**: Intégrer Cloudinary/AWS S3 pour les images
   
2. **Mémoire limitée**: 512MB-1GB selon le plan
   - **Solution**: Optimisation déjà faite (CPU-only, 1 worker)

3. **Base de données**: SQLite pas recommandée en prod
   - **Solution**: Migration vers PostgreSQL Railway (1 clic)

## 🔍 Endpoints Disponibles

- **`/`** : Page d'accueil
- **`/login`** : Authentification
- **`/register`** : Inscription
- **`/analyse`** : Analyse d'images
- **`/health`** : Healthcheck (Railway)

## 🛠️ Commandes Utiles

### Développement local:
```bash
./test-local.sh           # Test local
python app.py             # Démarrage dev
```

### Production Railway:
```bash
railway logs              # Voir les logs
railway open              # Ouvrir l'app
railway variables set SECRET_KEY=nouvelle_cle
```

## 🐛 Dépannage

### Erreurs courantes:

1. **Modèle YOLO non trouvé**
   ```bash
   # Vérifier la présence
   ls -lh *.pt
   ```

2. **Erreur de mémoire**
   - Réduire la taille d'image
   - Utiliser `confidence_threshold` plus élevé

3. **Erreur de base de données**
   ```bash
   # Re-initialiser
   rm instance/site.db
   python -c "from app import create_database; create_database()"
   ```

### Logs Railway:
```bash
railway logs --tail 100   # Derniers logs
railway logs --follow     # Temps réel
```

## 📈 Monitoring

L'application inclut:
- **Healthcheck automatique** : `/health`
- **Logs structurés** : Erreurs et performances
- **Métriques modèles** : Temps traitement, confiance

## 🔐 Sécurité

Configuration production inclut:
- **HTTPS forcé** : `PREFERRED_URL_SCHEME = 'https'`
- **Cookies sécurisés** : `SESSION_COOKIE_SECURE = True`
- **Variables d'environnement** : Secrets externalisés

---

## 🎉 Prêt pour Railway!

Votre application est maintenant **100% compatible Railway** avec:
- ✅ Configuration optimisée
- ✅ Modèles YOLO légers (13MB total)
- ✅ Scripts de déploiement automatisés
- ✅ Monitoring intégré
- ✅ Sécurité production

**Lancez `./deploy-railway.sh` pour commencer!**
