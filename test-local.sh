#!/bin/bash

echo "🧪 Test local de l'application avant déploiement Railway..."

# Vérifier Python
python --version

# Vérifier les dépendances
echo "📦 Vérification des dépendances..."
pip install -r requirements-railway.txt

# Vérifier la structure des fichiers
echo "📋 Vérification de la structure..."
required_files=("app.py" "routes.py" "models.py" "requirements-railway.txt" "Procfile" "start.sh")

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file manquant"
    fi
done

# Vérifier les modèles
if [ -f "best.pt" ]; then
    echo "✅ Modèle YOLO: best.pt"
else
    echo "⚠️  Modèle YOLO non trouvé: best.pt"
fi

# Test de syntaxe Python
echo "🐍 Test de syntaxe Python..."
python -m py_compile app.py routes.py models.py

# Test d'import
echo "📥 Test d'imports..."
python -c "
try:
    import flask
    import ultralytics
    import cv2
    import numpy
    print('✅ Tous les imports principaux fonctionnent')
except ImportError as e:
    print(f'❌ Erreur d\'import: {e}')
"

echo "✨ Tests terminés!"
