import time
import logging
import hcsr04sensor

# Set the debug level for RPi.GPIO library
logging.getLogger('RPi.GPIO').setLevel(logging.DEBUG)

def get_distance():
    # Create an instance of the HCSR04 sensor
    sensor = hcsr04sensor.HCSR04()

    # Perform distance measurement
    distance = sensor.distance_cm()

    return distance

def loop():
    while True:
        distance = get_distance()
        print("Gemessene Entfernung: {} cm".format(distance))
        time.sleep(1)

if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt:
        pass
