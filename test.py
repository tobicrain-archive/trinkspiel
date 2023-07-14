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
        print(f"\033[1;33m{i}\033[0m")  # Gelbe Textfarbe
        time.sleep(1)
    print("\033[1;32mWartezeit abgelaufen!\033[0m")  # Grüne Textfarbe

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
        input_wert = int(input("Geben Sie einen Min-Wert ein: "))

        max_input_wert = int(input("Geben Sie einen Max-Wert ein: "))
        zufallszahl = random.randint(input_wert, max_input_wert)
        print("\033[1;35mZufallszahl:", zufallszahl, "\033[0m")  # Violette Textfarbe
        countdown_sleep(5)

        versuche = 3
        trinken = False
        while versuche > 0:
            abstand = distanz()
            print("Gemessene Entfernung = %.1f cm" % abstand)
            toleranz = zufallszahl * 0.05  # Toleranz von 5%
            if zufallszahl - toleranz <= abstand <= zufallszahl + toleranz:
                print("\033[1;32mRichtige Distanz gehalten!\033[0m")  # Grüne Textfarbe
                break
            else:
                print("\033[1;31mFalsche Distanz gehalten!\033[0m")  # Rote Textfarbe
                versuche -= 1
                if versuche > 0:
                    print("Du hast noch", versuche, "Versuche.")
                    countdown_sleep(3)
                else:
                    trinken = True
                    print("\033[1;31mKeine Versuche mehr übrig. Das Spiel ist vorbei.\033[0m")  # Rote Textfarbe

        if trinken:
            print("\033[1;31mDu musst trinken!\033[0m")  # Rote Textfarbe
            
        GPIO.cleanup()

    # Beim Abbruch durch STRG+C zurücksetzen
    except KeyboardInterrupt:
        print("\n\033[1;33mMessung vom Benutzer gestoppt\033[0m")  # Gelbe Textfarbe
        GPIO.cleanup()
