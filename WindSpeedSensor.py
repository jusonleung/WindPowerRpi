import smbus2
import time
import threading

class WindSpeedSensor:
    def __init__(self, bus, pcf8591_i2c_addr, analog_pin):
        self.bus = bus
        self.pcf8591 = pcf8591_i2c_addr
        self.analog_pin = analog_pin
        self.windSpeed = 0
        # Exponential moving average filter parameter
        self.alpha = 0.2
        self.thread = threading.Thread(target=self.collect_wind_speed)
        self.thread.daemon = True
        
    def collect_wind_speed(self):
        while True:
            self.bus.write_byte(self.pcf8591,self.analog_pin)
            read = self.bus.read_byte(self.pcf8591)
            new_windSpeed = read * 625/4608
            if self.windSpeed == 0:
                self.windSpeed = new_windSpeed
            else:
                self.windSpeed = self.alpha * new_windSpeed +  (1 - self.alpha) * self.windSpeed
            time.sleep(0.5)
            
    def get_wind_speed(self):
        return self.windSpeed
    
    def start(self):
        self.thread.start()
    
#For testing
if __name__ == '__main__':
    bus = smbus2.SMBus(1)
    pcf8591_i2c_addr = 0x48
    A0 = 0x40
    A1 = 0x41
    A2 = 0x42
    A3 = 0x43
    windSpeed_Sensor = WindSpeedSensor(bus, pcf8591_i2c_addr, A0)
    windSpeed_Sensor.start()
    try:
        # Continuously print RPM readings
        while True:
            time.sleep(1)
            print(windSpeed_Sensor.get_wind_speed())
    except KeyboardInterrupt:
        print('end')
    