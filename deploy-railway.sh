#!/bin/bash

echo "🚀 Script de déploiement Railway pour l'application d'analyse médicale"
echo "=================================================================="

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher des messages colorés
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifications préalables
info "Vérification de l'environnement..."

# Vérifier Git
if ! command -v git &> /dev/null; then
    error "Git n'est pas installé"
    exit 1
fi

# Vérifier que nous sommes dans un repo git
if [ ! -d .git ]; then
    warning "Pas de repository Git détecté. Initialisation..."
    git init
    info "Repository Git initialisé"
fi

# Vérifier la présence des fichiers critiques
info "Vérification des fichiers critiques..."

critical_files=("app.py" "requirements.txt" "Procfile" "runtime.txt")
for file in "${critical_files[@]}"; do
    if [ ! -f "$file" ]; then
        error "Fichier manquant: $file"
        exit 1
    else
        info "✓ $file présent"
    fi
done

# Vérifier les modèles YOLO
info "Vérification des modèles YOLO..."
model_found=false
for model in best.pt best1.pt; do
    if [ -f "$model" ]; then
        size=$(du -h "$model" | cut -f1)
        info "✓ Modèle $model trouvé ($size)"
        model_found=true
    fi
done

if [ "$model_found" = false ]; then
    error "Aucun modèle YOLO trouvé (.pt)"
    exit 1
fi

# Optimiser requirements.txt pour Railway
if [ -f "requirements-railway.txt" ]; then
    info "Utilisation des requirements optimisés pour Railway..."
    cp requirements.txt requirements-dev.txt
    cp requirements-railway.txt requirements.txt
    info "requirements.txt optimisé pour Railway"
fi

# Préparer .gitignore
if [ ! -f .gitignore ]; then
    info "Création du .gitignore..."
    cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
instance/
.pytest_cache/
.env
.venv
venv/
ENV/
.DS_Store
*.log
EOF
fi

# Ajouter tous les fichiers
info "Préparation des fichiers pour Git..."
git add .

# Vérifier s'il y a des changements à commiter
if git diff --staged --quiet; then
    warning "Aucun changement détecté"
else
    info "Commit des changements..."
    git commit -m "Configuration pour déploiement Railway - $(date)"
fi

# Instructions pour Railway
echo ""
echo "🎯 PRÊT POUR LE DÉPLOIEMENT SUR RAILWAY!"
echo "======================================="
echo ""
echo "Étapes suivantes:"
echo "1. Connectez-vous sur https://railway.app"
echo "2. Créez un nouveau projet"
echo "3. Connectez votre repository GitHub"
echo "4. Railway détectera automatiquement votre app Python"
echo ""
echo "Variables d'environnement à configurer sur Railway:"
echo "- SECRET_KEY=votre_cle_secrete_super_secure"
echo "- RAILWAY_ENVIRONMENT=production"
echo "- CONFIDENCE_THRESHOLD=0.4 (optionnel)"
echo ""
echo "5. Déployez!"
echo ""
echo "📊 Informations du projet:"
echo "- Fichiers Python: $(find . -name '*.py' | wc -l)"
echo "- Modèles YOLO: $(find . -name '*.pt' | wc -l)"
echo "- Templates: $(find templates -name '*.html' 2>/dev/null | wc -l)"
echo "- Taille totale des modèles: $(du -ch *.pt 2>/dev/null | tail -1 | cut -f1)"
echo ""
info "Configuration terminée avec succès! 🎉"
