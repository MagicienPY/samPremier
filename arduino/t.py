from pyAudioAnalysis import audioTrainTest as aT
import os

# Chemin vers le dossier contenant les enregistrements vocaux d'authentification
chemin_dossier = "/home/magicien/Documents/testArduinoPythona/1.ogg"

def authentifier_voix():
    # Entraînement du modèle de reconnaissance vocale
    aT.extract_features_and_train([chemin_dossier], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "svm", "modele_authentification")

    # Enregistrement de la voix à authentifier
    os.system("rec enregistrement.wav")

    # Chargement du modèle de reconnaissance vocale
    modele = aT.load_model("modele_authentification")

    # Authentification de la voix
    resultat, _ = aT.file_classification("enregistrement.wav", modele, "svm")

    if resultat[0] == 1:
        print("Authentification réussie !")
    else:
        print("Voix non reconnue.")

# Appel de la fonction pour authentifier la voix
authentifier_voix()
