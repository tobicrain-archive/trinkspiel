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
        print(f"\033[1;33m{i}\033[0m", end='  ')  # Gelbe Textfarbe
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

def print_header():
    print("\033[1m\033[4m--- TRINKSPIEL ---\033[0m\n")  # Fettdruck und Unterstrich für den Header

def print_footer():
    print("\n\033[1m--- SPIEL BEENDET ---\033[0m")  # Fettdruck für den Footer

def print_info(message):
    print(f"\033[1;34m{message}\033[0m")  # Blaue Textfarbe für allgemeine Informationen

def print_success(message):
    print(f"\033[1;32m{message}\033[0m")  # Grüne Textfarbe für Erfolgsmeldungen

def print_error(message):
    print(f"\033[1;31m{message}\033[0m")  # Rote Textfarbe für Fehlermeldungen

if __name__ == '__main__':
    try:
        print_header()

        input_wert = int(input("Geben Sie einen Min-Wert ein: "))
        max_input_wert = int(input("Geben Sie einen Max-Wert ein: "))
        zufallszahl = random.randint(input_wert, max_input_wert)
        print_info(f"Zufallszahl: {zufallszahl}")
        countdown_sleep(5)

        versuche = 3
        trinken = False
        while versuche > 0:
            abstand = distanz()
            print(f"\nGemessene Entfernung = \033[1;35m{abstand:.1f} cm\033[0m")  # Violette Textfarbe
            toleranz = zufallszahl * 0.05  # Toleranz von 5%
            if zufallszahl - toleranz <= abstand <= zufallszahl + toleranz:
                print_success("Richtige Distanz gehalten!")
                break
            else:
                print_error("Falsche Distanz gehalten!")
                versuche -= 1
                if versuche > 0:
                    print_info(f"Du hast noch {versuche} Versuche.")
                    countdown_sleep(3)
                else:
                    trinken = True
                    print_error("Keine Versuche mehr übrig. Das Spiel ist vorbei.")

        if trinken:
            print_error("Du musst trinken!")

        print_footer()
        GPIO.cleanup()

    # Beim Abbruch durch STRG+C zurücksetzen
    except KeyboardInterrupt:
        print_info("\nMessung vom Benutzer gestoppt")
        GPIO.cleanup()
