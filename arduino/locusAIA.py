from pyfirmata import Arduino, util
#import MySQLdb
import time
import pymysql
import adafruit_dht
import datetime
import board
import pyttsx3 as pt


date1 = datetime.date.today()


carte = Arduino('/dev/ttyACM0')
acquisition = util.Iterator(carte)
acquisition.start()

tenssio =  carte.get_pin('a:0:i')

echo =  carte.get_pin('d:8:i')
trig =  carte.get_pin('d:9:o')

pin = carte.get_pin('d:7:o')
alert = carte.get_pin('d:2:o')

time.sleep(1.0)
sam = pt.init()

def photr():
    tenssion  =  tenssio.read()
    return tenssion


def ultrason():

    while True:
    # Envoyer une impulsion de 10µs sur la broche de déclenchement
        trig.write(1)
        time.sleep(0.00001)
        trig.write(0)

        # Attendre jusqu'à ce que le capteur envoie un signal
        while echo.read() == 0:
            debut_impulsion = time.time()

        # Mesurer le temps de retour de l'écho
        while echo.read() == 1:
            fin_impulsion = time.time()

        # Calculer la durée de l'impulsion
        duree_impulsion = fin_impulsion - debut_impulsion

        # Calculer la distance en utilisant la vitesse du son (343m/s)
        distance = (duree_impulsion * 34300) / 2

        # Afficher la distance
        print("Distance :", distance, "cm")

        # Attendre 1 seconde avant de mesurer à nouveau
        time.sleep(1)
        pin.write(1)
        if (distance < 150):
            sam.say("attention objet detecte à,")
            sam.say(distance)
            sam.say(" centimètre")
            sam.runAndWait() 


        

def temperature():

    dht = adafruit_dht.DHT22(board.D12)
    try:
    # Lecture de la température et de l'humidité
        temperature = dht.temperature
        humidity = dht.humidity

        # Affichage des valeurs
        print("Température : {:.1f} °C".format(temperature))
        print("Humidité : {:.1f} %".format(humidity))

    except RuntimeError as error:
        # Gestion des erreurs de lecture
        print("Erreur de lecture du capteur DHT :", error.args[0])

    except Exception as error:
        # Gestion des autres erreurs
        print("Erreur :", error)

    finally:
        # Fermeture du capteur
        dht.exit()
ultrason()
#temperature()