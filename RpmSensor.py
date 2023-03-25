import RPi.GPIO as GPIO
import time
import threading

class RpmSensor:
    def __init__(self, pin):
        # Initialize variables and constants
        self.pin = pin
        self.sticker_detected = False
        self.revolution = 0
        self.rpm = 0
        self.alpha = 0.2 # Exponential moving average filter parameter
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
                # Initialize detection and calculation threads
        self.detect_thread = threading.Thread(target=self.detect_sticker)
        self.calculate_thread = threading.Thread(target=self.calculate_rpm)
        self.detect_thread.daemon = True
        self.calculate_thread.daemon = True
        
        # Initialize last time variable for elapsed time calculation
        self.last_time = 0

    def detect_sticker(self):
        # Continuously detect obstacles and increment revolution count
        self.last_time = time.time_ns()
        while True:
            if not GPIO.input(self.pin) and not self.sticker_detected:
                self.sticker_detected = True
            elif GPIO.input(self.pin) and self.sticker_detected:
                self.sticker_detected = False
                self.revolution += 1
            time.sleep(0.005)

    def calculate_rpm(self):
        # Calculate RPM using exponential moving average filter
        while True:
            time.sleep(1)
            elapsed_time = time.time_ns() - self.last_time
            num_revolutions = self.revolution
            self.last_time = time.time_ns()
            self.revolution = 0
            new_rpm = ((num_revolutions / elapsed_time ) * 60000000000 )
            if new_rpm >= 0:
                self.rpm = self.alpha * self.rpm + (1 - self.alpha) * new_rpm

    def get_rpm(self):
        return self.rpm

    def start(self):
        # Start detection and calculation threads
        self.detect_thread.start()
        self.calculate_thread.start()

#For testing
if __name__ == '__main__':
    # Create and start RPM sensor object
    ir_sensor = RpmSensor(18)
    ir_sensor.start()
    time.sleep(2)
    try:
        # Continuously print RPM readings
        while True:
            time.sleep(1)
            print(ir_sensor.get_rpm())
    except KeyboardInterrupt:
        GPIO.cleanup()