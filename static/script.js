// static/script.js

// --- Code Sidebar (inchangé) ---
const sidebar = document.getElementById('sidebar');
const sidebarBackdrop = document.getElementById('sidebarBackdrop');
const toggleSidebarMobileButton = document.getElementById('toggleSidebarMobile');

if (sidebar && toggleSidebarMobileButton && sidebarBackdrop) {
    const toggleSidebar = () => {
        sidebar.classList.toggle('hidden');
        sidebarBackdrop.classList.toggle('hidden');
    };

    toggleSidebarMobileButton.addEventListener('click', toggleSidebar);
    sidebarBackdrop.addEventListener('click', toggleSidebar);
}

// --- Code pour faire disparaître les messages flash (inchangé) ---
document.addEventListener('DOMContentLoaded', () => {
    const alertElements = document.querySelectorAll('.alert');

    alertElements.forEach(alert => {
        setTimeout(() => {
            alert.style.display = 'none';
        }, 5000);
    });


    // --- Code pour gérer le flux de la page d'analyse ---
    const uploadSection = document.getElementById('upload-section');
    const imagePreviewSection = document.getElementById('image-preview-section');
    const resultatsSection = document.getElementById('resultats-section');
    const patientInfoFormSection = document.getElementById('patient-info-form-section');
    const imageUploadInput = document.getElementById('image_upload');
    const imagePreviewElement = document.getElementById('image-preview');
    const uploadButton = document.getElementById('upload-button');
    const analyseButton = document.getElementById('analyse-button');
    const saveButton = document.getElementById('save-button'); // Bouton "Sauvegarder les résultats" (hors formulaire patient)
    const saveFormButton = document.getElementById('save-form-button'); // Bouton "Confirmer et Sauvegarder" (dans formulaire patient)
    const uploadForm = document.getElementById('upload-form');
    const loadingIndicator = document.getElementById('loading-indicator');


    // --- Écouteur d'événement sur le bouton "Télécharger l'image" (inchangé) ---
    uploadButton.addEventListener('click', (event) => {
        event.preventDefault();
        imageUploadInput.click();
    });

    // --- Écouteur d'événement sur le changement de l'input type="file" (image_upload) ---
    imageUploadInput.addEventListener('change', () => {
        console.log("imageUploadInput.addEventListener('change') déclenché!");
        const file = imageUploadInput.files[0];
        if (file) {
            console.log("Fichier sélectionné:", file);
            const reader = new FileReader();
            reader.onload = (e) => {
                console.log("FileReader.onload exécuté!");
                console.log("Data URL:", e.target.result);
                imagePreviewElement.src = e.target.result;
                uploadSection.classList.add('hidden'); // Cache la section de téléchargement
                imagePreviewSection.classList.remove('hidden');
                analyseButton.classList.remove('hidden');
                console.log("Sections UI mises à jour (uploadSection caché, imagePreviewSection et analyseButton affichés)");
            };
            reader.readAsDataURL(file);
            console.log("FileReader.readAsDataURL(file) appelé!");
        } else {
            console.log("Aucun fichier sélectionné.");
        }
    });


    // --- Écouteur d'événement sur le bouton "Analyser l'image" (MODIFIÉ) ---
    analyseButton.addEventListener('click', () => {
        console.log("Bouton 'Analyser l'image' cliqué!");
        imagePreviewSection.classList.add('hidden');
        loadingIndicator.classList.remove('hidden');
        uploadForm.submit(); // Soumission du formulaire pour l'analyse (garde le comportement précédent)
    });

    // --- Écouteur d'événement sur le bouton "Sauvegarder les résultats" (MODIFIÉ) ---
    saveButton.addEventListener('click', () => {
        console.log("Bouton 'Sauvegarder les résultats' cliqué!");
        patientInfoFormSection.classList.remove('hidden'); // Affiche le formulaire patient
        saveButton.classList.add('hidden'); // Cache le bouton "Sauvegarder les résultats" lui-même
    });

    // --- Cacher initialement la section des infos patient et le bouton "Sauvegarder" (MODIFIÉ) ---
    patientInfoFormSection.classList.add('hidden');
    if (saveButton) { // Vérification pour éviter les erreurs si le bouton n'est pas rendu initialement
        saveButton.classList.add('hidden'); // Cache initialement le bouton "Sauvegarder les résultats"
    }


    // --- Afficher le bouton "Sauvegarder" seulement s'il y a des résultats d'analyse (MODIFIÉ) ---
    if (resultatsSection) {
        if (resultatsSection.children.length > 0) { // Vérifie si la section des résultats a du contenu (résultats affichés)
            saveButton.classList.remove('hidden'); // Affiche le bouton "Sauvegarder" seulement SI des résultats sont affichés

            // --- AJOUT IMPORTANT : Cacher définitivement les sections de téléchargement et prévisualisation ---
            uploadSection.classList.add('hidden');
            imagePreviewSection.classList.add('hidden');
        } else {
            saveButton.classList.add('hidden'); // S'assure que le bouton est caché s'il n'y a pas de résultats
        }
    }

    // --- AJOUT : Cacher les sections upload et preview au chargement de la page SI resultat_analyse existe déjà ---
    if (resultatsSection && resultatsSection.children.length > 0) {
        uploadSection.classList.add('hidden');
        imagePreviewSection.classList.add('hidden');
    }
});