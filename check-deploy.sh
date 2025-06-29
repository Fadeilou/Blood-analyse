#!/bin/bash

echo "🔍 VÉRIFICATION FINALE AVANT DÉPLOIEMENT RAILWAY"
echo "==============================================="

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction de vérification
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅ $1${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 MANQUANT${NC}"
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✅ $1/${NC}"
        return 0
    else
        echo -e "${RED}❌ $1/ MANQUANT${NC}"
        return 1
    fi
}

echo -e "${BLUE}📁 Vérification des fichiers critiques...${NC}"
CRITICAL_FILES=(
    "app.py"
    "requirements.txt"
    "Procfile"
    "runtime.txt"
    "railway.toml"
    "start.sh"
)

all_critical_ok=true
for file in "${CRITICAL_FILES[@]}"; do
    if ! check_file "$file"; then
        all_critical_ok=false
    fi
done

echo -e "\n${BLUE}🧠 Vérification des modèles YOLO...${NC}"
MODEL_FILES=(
    "best.pt"
    "best1.pt"
)

models_ok=true
for model in "${MODEL_FILES[@]}"; do
    if [ -f "$model" ]; then
        size=$(du -h "$model" | cut -f1)
        echo -e "${GREEN}✅ $model (${size})${NC}"
    else
        echo -e "${RED}❌ $model MANQUANT${NC}"
        models_ok=false
    fi
done

echo -e "\n${BLUE}📂 Vérification des dossiers...${NC}"
DIRS=(
    "static"
    "templates"
    "static/uploaded_images"
    "static/results_images"
)

dirs_ok=true
for dir in "${DIRS[@]}"; do
    if ! check_dir "$dir"; then
        dirs_ok=false
    fi
done

echo -e "\n${BLUE}🐍 Vérification Python...${NC}"
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version)
    echo -e "${GREEN}✅ $python_version${NC}"
else
    echo -e "${RED}❌ Python3 non trouvé${NC}"
fi

echo -e "\n${BLUE}📦 Vérification requirements.txt...${NC}"
if [ -f "requirements.txt" ]; then
    flask_line=$(grep "Flask==" requirements.txt)
    gunicorn_line=$(grep "gunicorn==" requirements.txt)
    
    if [ ! -z "$flask_line" ]; then
        echo -e "${GREEN}✅ $flask_line${NC}"
    else
        echo -e "${RED}❌ Flask manquant dans requirements.txt${NC}"
    fi
    
    if [ ! -z "$gunicorn_line" ]; then
        echo -e "${GREEN}✅ $gunicorn_line${NC}"
    else
        echo -e "${RED}❌ Gunicorn manquant dans requirements.txt${NC}"
    fi
fi

echo -e "\n${BLUE}🔧 Vérification Procfile...${NC}"
if [ -f "Procfile" ]; then
    if grep -q "gunicorn" Procfile; then
        echo -e "${GREEN}✅ Procfile contient gunicorn${NC}"
    else
        echo -e "${RED}❌ Procfile ne contient pas gunicorn${NC}"
    fi
fi

echo -e "\n${BLUE}🚀 Vérification Git...${NC}"
if [ -d ".git" ]; then
    echo -e "${GREEN}✅ Repository Git initialisé${NC}"
    
    # Vérifier s'il y a des changements non commitées
    if git diff --quiet && git diff --staged --quiet; then
        echo -e "${GREEN}✅ Tous les changements sont commitées${NC}"
    else
        echo -e "${YELLOW}⚠️  Il y a des changements non commitées${NC}"
        echo -e "${YELLOW}   Exécutez: git add . && git commit -m 'Final config'${NC}"
    fi
    
    # Vérifier la branche
    current_branch=$(git branch --show-current)
    echo -e "${GREEN}✅ Branche actuelle: $current_branch${NC}"
else
    echo -e "${RED}❌ Pas de repository Git${NC}"
    echo -e "${YELLOW}   Exécutez: git init${NC}"
fi

echo -e "\n${BLUE}📊 Statistiques du projet...${NC}"
if command -v find &> /dev/null; then
    py_files=$(find . -name "*.py" | wc -l)
    html_files=$(find . -name "*.html" | wc -l)
    total_size=$(du -sh . | cut -f1)
    
    echo -e "${GREEN}📁 Fichiers Python: $py_files${NC}"
    echo -e "${GREEN}🌐 Templates HTML: $html_files${NC}"
    echo -e "${GREEN}💾 Taille totale: $total_size${NC}"
fi

echo -e "\n${BLUE}===============================================${NC}"
if [ "$all_critical_ok" = true ] && [ "$models_ok" = true ] && [ "$dirs_ok" = true ]; then
    echo -e "${GREEN}🎉 TOUT EST PRÊT POUR RAILWAY! 🚀${NC}"
    echo -e "${GREEN}Vous pouvez maintenant déployer sur https://railway.app${NC}"
    echo -e "\n${YELLOW}Étapes suivantes:${NC}"
    echo -e "1. git push origin main"
    echo -e "2. Aller sur railway.app"
    echo -e "3. Deploy from GitHub repo"
    echo -e "4. Configurer les variables d'environnement"
    echo -e "5. Déployer! 🎯"
else
    echo -e "${RED}❌ IL Y A DES PROBLÈMES À CORRIGER${NC}"
    echo -e "${YELLOW}Corrigez les erreurs ci-dessus avant de déployer${NC}"
fi

echo -e "\n${BLUE}📖 Consultez DEPLOIEMENT-FINAL.md pour plus de détails${NC}"
