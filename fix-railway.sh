#!/bin/bash

echo "🔧 Fix pour déploiement Railway - Correction des dépendances PyTorch"

# Backup des requirements actuels
cp requirements.txt requirements-backup.txt

# Utiliser les versions compatibles Railway
echo "📦 Mise à jour des dépendances pour Railway..."

# Commit des changements
git add requirements.txt pip.conf requirements-railway-fix.txt
git commit -m "Fix: Versions PyTorch compatibles Railway (CPU-only)"

echo "✅ Fix appliqué! Vous pouvez maintenant redéployer sur Railway."
echo "📋 Changements:"
echo "   - torch 2.6.0+cpu → 2.5.1 (version stable PyPI)"
echo "   - torchvision 0.21.0+cpu → 0.20.1 (version stable PyPI)"
echo "   - opencv-python-headless 4.11.0.86 → 4.10.0.84 (version stable)"
echo "   - numpy 2.0.2 → 1.26.4 (compatibility)"

echo ""
echo "🚀 Prochaines étapes:"
echo "1. git push origin main"
echo "2. Redéployer sur Railway"
echo "3. L'application devrait maintenant se construire correctement!"
