import RPi.GPIO as GPIO
import time
import random

# GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# GPIO Pins zuweisen
GPIO_TRIGGER = 18
GPIO_ECHO = 24

# Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def countdown_sleep(seconds):
    for i in range(seconds, 0, -1):
        print(i)
        time.sleep(1)
    print("Wartezeit abgelaufen!")

def distanz():
    # Setze Trigger auf HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # Setze Trigger nach 0.01ms auf LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartZeit = time.time()
    StopZeit = time.time()

    # Speichere Startzeit
    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()

    # Speichere Ankunftszeit
    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()

    # Zeitdifferenz zwischen Start und Ankunft
    TimeElapsed = StopZeit - StartZeit
    # Mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurück
    distanz = (TimeElapsed * 34300) / 2

    return distanz

if __name__ == '__main__':
    try:
        input_wert = int(input("Geben Sie einen Wert ein: "))
        zufallszahl = random.randint(1, input_wert)
        print("Zufallszahl:", zufallszahl)
        countdown_sleep(5)

        versuche = 3
        while versuche > 0:
            abstand = distanz()
            print("Gemessene Entfernung = %.1f cm" % abstand)
            toleranz = zufallszahl * 0.05  # Toleranz von 2-3%
            if zufallszahl - toleranz <= abstand <= zufallszahl + toleranz:
                print("Richtige Distanz gehalten!")
                break
            else:
                print("Falsche Distanz gehalten. Du musst trinken!")
                versuche -= 1
                if versuche > 0:
                    print("Du hast noch", versuche, "Versuche.")
                    countdown_sleep(3)
                else:
                    print("Keine Versuche mehr übrig. Das Spiel ist vorbei.")
            
        GPIO.cleanup()

    # Beim Abbruch durch STRG+C zurücksetzen
    except KeyboardInterrupt:
        print("Messung vom Benutzer gestoppt")
        GPIO.cleanup()
