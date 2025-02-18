from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy() # Instance SQLAlchemy pour toute l'application

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False) # Stocker les hash de mots de passe en production !
    analyses = db.relationship('AnalyseResult', backref='technicien', lazy=True) # Relation avec AnalyseResult

    def __repr__(self):
        return f"User('{self.username}')"

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100))
    date_naissance = db.Column(db.Date) # Ajouter d'autres infos patient si nécessaire
    analyses = db.relationship('AnalyseResult', backref='patient', lazy=True) # Relation avec AnalyseResult

    def __repr__(self):
        return f"Patient('{self.nom} {self.prenom}')"

class AnalyseResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String(200), nullable=False) # Nom du fichier image stocké
    date_analyse = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    test_positif = db.Column(db.Boolean, nullable=False)
    type_anomalie = db.Column(db.String(100)) # Drépanocytes, Schizocytes, Elliptocytes, None si négatif
    recommandation = db.Column(db.Text) # Recommandation basée sur l'analyse
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False) # Clé étrangère vers Patient
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Clé étrangère vers User (Technicien)

    def __repr__(self):
        return f"AnalyseResult(date_analyse='{self.date_analyse}', test_positif={self.test_positif}, patient_id={self.patient_id}, user_id={self.user_id})"