import RPi.GPIO as GPIO
import time

# GPIO-Pins für den Ultraschallsensor festlegen
trigger_pin = 23
echo_pin = 24

# GPIO-Modus festlegen
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

def messen_entfernung():
    # Trigger-Pin auf High setzen
    GPIO.output(trigger_pin, True)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, False)

    startzeit = time.time()
    endzeit = time.time()

    # Echo-Pin-Dauer messen
    while GPIO.input(echo_pin) == 0:
        startzeit = time.time()
    while GPIO.input(echo_pin) == 1:
        endzeit = time.time()

    dauer = endzeit - startzeit

    # Schallgeschwindigkeit (34300 cm/s) einbeziehen, um Entfernung zu berechnen
    entfernung = (dauer * 34300) / 2

    return entfernung

def trinkspiel():
    # Schwellenwert für die Entfernung festlegen
    schwellenwert = 20

    print("Willkommen beim Trinkspiel!")
    print("Versuche, deine Hand vor den Ultraschallsensor zu halten.")
    print("Wenn du es schaffst, gewinnst du!")

    while True:
        entfernung = messen_entfernung()

        if entfernung < schwellenwert:
            print("Gewonnen! Du darfst trinken!")
        else:
            print("Leider verloren. Weiterhin nüchtern bleiben!")

        time.sleep(1)

try:
    trinkspiel()
except KeyboardInterrupt:
    GPIO.cleanup()
