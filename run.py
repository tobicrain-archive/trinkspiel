import RPi.GPIO as GPIO
import time

# GPIO-Pins für den Ultraschallsensor festlegen
TRIGGER_PIN = 23
ECHO_PIN = 24

def setup():
    # GPIO initialisieren
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIGGER_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

def get_distance():
    # Trigger-Pin kurzzeitig auf High setzen
    GPIO.output(TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)

    # Startzeitpunkt festhalten
    pulse_start = time.time()

    # Warten, bis das Echo-Pin auf High wechselt
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    # Warten, bis das Echo-Pin auf Low wechselt
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # Dauer des Ultraschallpulses berechnen
    pulse_duration = pulse_end - pulse_start

    # Entfernung in Zentimetern berechnen (Schallgeschwindigkeit: 34300 cm/s)
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def loop():
    while True:
        distance = get_distance()
        print("Gemessene Entfernung: {} cm".format(distance))
        time.sleep(1)

def cleanup():
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        cleanup()
