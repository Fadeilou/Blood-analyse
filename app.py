from flask import Flask
from routes import routes
from models import db # Importe l'instance de base de données depuis models.py
from flask_login import LoginManager
import os
from config import config

app = Flask(__name__)

# Configuration selon l'environnement
config_name = os.environ.get('FLASK_ENV', 'default')
if os.environ.get('RAILWAY_ENVIRONMENT'):
    config_name = 'production'

app.config.from_object(config[config_name])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['UPLOAD_FOLDER'] = 'static/uploaded_images' # Configure UPLOAD_FOLDER here

app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploaded_images') # Chemin plus robuste
app.config['RESULTS_FOLDER'] = os.path.join(app.static_folder, 'results_images') # Chemin vers les images résultat

# Créer les dossiers si n'existent pas au démarrage
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)


db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'routes.login'
login_manager.login_message_category = 'info'
login_manager.init_app(app)

app.register_blueprint(routes)

# Healthcheck endpoint pour Railway
@app.route('/health')
def health_check():
    """Endpoint de santé pour Railway"""
    try:
        # Vérifier la base de données
        with app.app_context():
            db.engine.execute('SELECT 1')
        
        # Vérifier les modèles
        from model_config import ModelConfig
        available_models = ModelConfig.list_available_models()
        
        return {
            'status': 'healthy',
            'database': 'connected',
            'models_available': len(available_models),
            'models': [m['name'] for m in available_models]
        }, 200
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }, 500

from models import User, Patient, AnalyseResult # noqa

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_database():
    with app.app_context():
        db.create_all()
        print('Base de données créée!')

if __name__ == '__main__':
    create_database()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)