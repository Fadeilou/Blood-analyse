from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import random
from models import db, User, Patient, AnalyseResult
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from forms import RegistrationForm
from login_form import LoginForm
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Sequential, load_model # Importez Sequential de Keras # NOUVEAU : Importez Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Activation, Dropout, ZeroPadding2D, BatchNormalization # Inclure Flatten dans l'import # NOUVEAU : Ajout de Flatten dans l'import
import pdb

routes = Blueprint('routes', __name__)

# --- Définition de l'architecture AlexNet CNN (REPRODUITE DEPUIS LE NOTEBOOK) --- # NOUVEAU : Définition de l'architecture du modèle CNN
def create_alexnet_model(input_shape, n_classes, base_filter):
    classifier = Sequential()

    classifier.add(tf.keras.layers.Conv2D(base_filter, (5, 5), activation='relu', input_shape=input_shape))
    classifier.add(tf.keras.layers.Conv2D(2*base_filter, (5, 5), activation='relu'))
    classifier.add(tf.keras.layers.MaxPooling2D(pool_size=(1, 1)))
    classifier.add(tf.keras.layers.ZeroPadding2D((1,1)))

    classifier.add(tf.keras.layers.Conv2D(4*base_filter, (4, 4), activation='relu'))
    classifier.add(tf.keras.layers.MaxPooling2D(pool_size=(1, 1)))
    classifier.add(tf.keras.layers.ZeroPadding2D((1,1)))

    classifier.add(tf.keras.layers.Conv2D(4*base_filter, (4, 4), activation='relu'))
    classifier.add(tf.keras.layers.ZeroPadding2D((1,1)))

    classifier.add(tf.keras.layers.Conv2D(2*base_filter, (3, 3), activation='relu'))
    classifier.add(tf.keras.layers.ZeroPadding2D((1,1)))

    classifier.add(tf.keras.layers.Conv2D(base_filter, (3, 3), activation='relu'))
    classifier.add(tf.keras.layers.ZeroPadding2D((1,1)))
    classifier.add(tf.keras.layers.MaxPooling2D(pool_size=(1, 1)))

    classifier.add(tf.keras.layers.Conv2D(base_filter, (3, 3), activation='relu'))
    classifier.add(tf.keras.layers.ZeroPadding2D((1,1)))
    classifier.add(tf.keras.layers.MaxPooling2D(pool_size=(1, 1)))

    classifier.add(tf.keras.layers.Conv2D(base_filter, (2, 2), activation='relu'))
    classifier.add(tf.keras.layers.ZeroPadding2D((1,1)))
    classifier.add(tf.keras.layers.MaxPooling2D(pool_size=(1, 1)))

    classifier.add(tf.keras.layers.Conv2D(base_filter, (2, 2), activation='relu'))
    classifier.add(tf.keras.layers.ZeroPadding2D((1,1)))
    classifier.add(tf.keras.layers.MaxPooling2D(pool_size=(1, 1)))

    classifier.add(tf.keras.layers.Conv2D(base_filter, (2, 2), activation='relu'))
    classifier.add(tf.keras.layers.ZeroPadding2D((1,1)))
    classifier.add(tf.keras.layers.MaxPooling2D(pool_size=(1, 1)))

    classifier.add(tf.keras.layers.Conv2D(base_filter, (2, 2), activation='relu'))
    classifier.add(tf.keras.layers.ZeroPadding2D((1,1)))
    classifier.add(tf.keras.layers.MaxPooling2D(pool_size=(1, 1)))

    classifier.add(Flatten())

    classifier.add(Dense(units=16*base_filter, activation='relu'))
    classifier.add(Dropout(rate=0.5))

    classifier.add(Dense(units=32*base_filter, activation='relu'))
    classifier.add(Dropout(rate=0.5))

    classifier.add(Dense(units=64*base_filter, activation='relu'))
    classifier.add(Dropout(rate=0.5))

    classifier.add(Dense(units=n_classes, activation='softmax'))

    return classifier


# Chargement du modèle CNN (variable globale) - MODIFIÉ - Utilise la fonction create_alexnet_model pour définir l'architecture AVANT de charger les poids
model_cnn = None
def load_cnn_model():
    global model_cnn
    try:
        input_shape = (128, 128, 3) # Taille d'entrée des images (image_height, image_width, n_channels)
        n_classes = 3 # Nombre de classes (Drépanocytes, Elliptocytes, Schizocytes)
        base_filter = 20 # Base filter size (comme dans le notebook)
        model_cnn = create_alexnet_model(input_shape, n_classes, base_filter) # Crée l'architecture AlexNet AVANT de charger les poids # NOUVEAU : Crée l'architecture AlexNet
        model_cnn.load_weights('alexnet_32.h5') # Charge les poids sauvegardés dans l'architecture AlexNet # NOUVEAU : Charge les poids dans l'architecture AlexNet
        print("Modèle CNN chargé avec succès! (dans routes.py, architecture AlexNet reproduite)") # Message mis à jour pour indiquer que l'architecture AlexNet est reproduite
    except Exception as e:
        print(f"Erreur lors du chargement du modèle CNN: {e} (dans routes.py)")
        model_cnn = None

load_cnn_model() # Appelle la fonction pour charger le modèle au démarrage du module routes.py


# --- Authentification ---
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Connexion réussie!', 'success')
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Login incorrect. Veuillez vérifier votre nom d\'utilisateur et votre mot de passe.', 'danger')
    return render_template('login.html', title='Connexion', form=form, logged_out_content=True)

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Votre compte a été créé avec succès! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('routes.login'))
    return render_template('register.html', title='Inscription', form=form, logged_out_content=True)

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Déconnexion réussie.', 'info')
    return redirect(url_for('routes.login'))

# --- Dashboard Routes ---
@routes.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html', title='Tableau de Bord - Analyse', dashboard_content=True)

@routes.route('/')
@login_required
def index_redirect_dashboard():
    return redirect(url_for('routes.dashboard'))

@routes.route('/analyses')
@login_required
def analyses_list():
    analyses = AnalyseResult.query.filter_by(user_id=current_user.id).order_by(AnalyseResult.date_analyse.desc()).all()
    return render_template('analyses_list.html', analyses=analyses, title='Tableau de Bord - Liste des Analyses', dashboard_content=True)

@routes.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Tableau de Bord - Profil', dashboard_content=True)


# --- Route Page d'Analyse (Mise à Jour - Modèle CNN chargé dans routes.py) ---
@routes.route('/analyse', methods=['GET', 'POST'])
@login_required
def analyse():
    resultat_analyse = None
    patient_info = {}
    image_filename = None

    if request.method == 'POST':
        if 'image_upload' not in request.files:
            flash('Aucun fichier image sélectionné.', 'danger')
        else:
            image_file = request.files['image_upload']
            if image_file.filename == '':
                flash('Aucun fichier image sélectionné.', 'danger')
            elif allowed_file(image_file.filename):
                try:
                    # --- Analyse de l'image avec le modèle CNN (utilisation de la nouvelle fonction analyse_image) ---
                    resultat_analyse_dict = analyse_image(image_file) # Appelle la fonction analyse_image (qui utilise maintenant le modèle CNN avec l'architecture AlexNet reproduite)
                    resultat_analyse = resultat_analyse_dict
                    image_filename = image_file.filename
                except Exception as e:
                    flash(f"Erreur lors de l'analyse de l'image: {e}", 'danger')
                    resultat_analyse = None
            else:
                flash('Type de fichier non autorisé. Seuls les fichiers image sont acceptés.', 'danger')

    return render_template('index.html', resultat_analyse=resultat_analyse, patient_info=patient_info, title='Tableau de Bord - Analyse', dashboard_content=True, image_filename=image_filename)


# --- Fonction pour l'analyse d'image avec le modèle CNN (MODIFIÉE - Utilise l'architecture AlexNet reproduite) ---
def analyse_image(image_file):
    try:
        img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        img_resized = cv2.resize(img, (128, 128))
        img_array = image.img_to_array(img_resized)
        img_expanded = np.expand_dims(img_array, axis=0)
        # img_preprocessed = tf.keras.applications.resnet50.preprocess_input(img_expanded) # Pré-traitement ResNet50 - PROBABLEMENT NON NÉCESSAIRE POUR ALEXNET, SUPPRIMÉ
        img_preprocessed = img_expanded # PAS DE PRÉ-TRAITEMENT POUR L'INSTANT (à adapter si nécessaire)

        

        prediction = model_cnn.predict(img_preprocessed) # Utilise model_cnn (variable globale chargée dans routes.py - avec l'architecture AlexNet reproduite)
        # pdb.set_trace()
        predicted_class_index = np.argmax(prediction[0])

        print(f"Prédiction CNN: {prediction} - Index de classe prédite: {predicted_class_index}")

        cell_types = ["Drépanocytes", "Elliptocytes", "Schizocytes"]
        predicted_cell_type = cell_types[predicted_class_index] if predicted_class_index < len(cell_types) else "Inconnu"
        test_positif = predicted_cell_type != "Inconnu"

        if predicted_cell_type == "Drépanocytes":
            recommandation = "Présence de drépanocytes détectée. Électrophorèse de l'hémoglobine recommandée."
        elif predicted_cell_type == "Elliptocytes":
            recommandation = "Présence d'elliptocytes détectée. Examens complémentaires à envisager."
        elif predicted_cell_type == "Schizocytes":
            recommandation = "Présence de schizocytes détectée. Nécessite une investigation approfondie."
        else:
            recommandation = "Globules rouges normaux détectés. Test négatif."

        return {
            "test_positif": test_positif,
            "type_anomalie": predicted_cell_type if test_positif else None,
            "recommandation": recommandation if test_positif else "Aucune recommandation particulière."
        }

    except Exception as e:
        print(f"Erreur lors de l'analyse de l'image avec le modèle CNN: {e}")
        raise Exception(f"Erreur lors de l'analyse de l'image: {e}")


# --- Fonctions de vérification du type de fichier autorisé (inchangées) ---
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Nouvelle route pour la sauvegarde des résultats et des infos patient ---
@routes.route('/save_analysis', methods=['POST'])
@login_required
def save_analysis():
    if request.method == 'POST':
        patient_nom = request.form['patient_nom']
        patient_prenom = request.form['patient_prenom']
        patient_date_naissance_str = request.form['patient_date_naissance']
        patient_date_naissance = None
        if patient_date_naissance_str:
            patient_date_naissance = date.fromisoformat(patient_date_naissance_str)
        image_filename = request.form['image_filename']
        test_positif_str = request.form['test_positif']
        type_anomalie = request.form['type_anomalie']
        recommandation = request.form['recommandation']

        test_positif = test_positif_str.lower() == 'true'

        patient = Patient(nom=patient_nom, prenom=patient_prenom, date_naissance=patient_date_naissance)
        db.session.add(patient)
        db.session.flush()
        patient_id = patient.id

        analyse_result = AnalyseResult(
            image_filename=image_filename,
            test_positif=test_positif,
            type_anomalie=type_anomalie,
            recommandation=recommandation,
            patient_id=patient_id,
            user_id=current_user.id
        )
        db.session.add(analyse_result)
        db.session.commit()

        flash('Résultats de l\'analyse sauvegardés avec succès pour le patient!', 'success')
        return redirect(url_for('routes.analyses_list'))
    return redirect(url_for('routes.dashboard'))

