#!/bin/bash

echo "🚀 Démarrage de l'application d'analyse médicale..."

# Créer les dossiers nécessaires
echo "📁 Création des dossiers..."
mkdir -p static/uploaded_images
mkdir -p static/results_images

# Vérifier la présence des modèles
if [ -f "best.pt" ]; then
    echo "✅ Modèle YOLO trouvé: best.pt"
else
    echo "⚠️  Modèle YOLO non trouvé: best.pt"
fi

if [ -f "best1.pt" ]; then
    echo "✅ Modèle alternatif trouvé: best1.pt"
fi

# Initialiser la base de données
echo "🗄️  Initialisation de la base de données..."
python -c "
try:
    from app import create_database
    create_database()
    print('✅ Base de données initialisée avec succès')
except Exception as e:
    print(f'❌ Erreur lors de l\'initialisation de la base de données: {e}')
"

# Variables d'environnement par défaut
export FLASK_ENV=${FLASK_ENV:-production}
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8080}

echo "🌐 Démarrage du serveur sur ${HOST}:${PORT}"

# Démarrer l'application avec gunicorn
exec gunicorn \
    --bind ${HOST}:${PORT} \
    --workers 1 \
    --timeout 300 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --preload \
    --log-level info \
    app:app
