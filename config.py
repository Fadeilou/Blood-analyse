import os
from urllib.parse import urlparse

class Config:
    """Configuration de base pour l'application."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une_cle_secrete_tres_secrete'
    
    # Configuration base de données
    if os.environ.get('DATABASE_URL'):
        # Railway PostgreSQL
        database_url = os.environ.get('DATABASE_URL')
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # SQLite local
        SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Configuration YOLO
    MODEL_PATH = os.environ.get('MODEL_PATH', 'best.pt')
    CONFIDENCE_THRESHOLD = float(os.environ.get('CONFIDENCE_THRESHOLD', '0.4'))

class DevelopmentConfig(Config):
    """Configuration pour le développement."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

class ProductionConfig(Config):
    """Configuration pour la production."""
    DEBUG = False
    
    # Configuration spécifique à Railway
    PREFERRED_URL_SCHEME = 'https'
    
    # Augmenter les timeouts pour les modèles ML
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes
    
    # Configuration sécurité
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
class TestingConfig(Config):
    """Configuration pour les tests."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
