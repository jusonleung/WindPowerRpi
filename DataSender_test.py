import time
from RpmSensor import RpmSensor
from WindSpeedSensor import WindSpeedSensor
from GPS import GPS
from ElectricMeter import ElectricMeter
import smbus2
import threading
import datetime
import requests


class DataSender:

    # Analog
    pcf8591 = 0x48
    A0 = 0x40
    A1 = 0x41
    A2 = 0x42
    A3 = 0x43

    webAPI_url = 'https://windpowerwebapp.azurewebsites.net/api/SystemData'

    def __init__(self, interval=5):
        self.interval = interval
        self.RpmSensor = RpmSensor(18)
        self.bus = smbus2.SMBus(1)
        self.WindSpeedSensor = WindSpeedSensor(self.bus, self.pcf8591, self.A0)
        # self.GPS = GPS("/dev/ttyUSB2")
        # self.generator_meter = ElectricMeter("/dev/ttyUSB0")
        # self.inverter_meter = ElectricMeter("/dev/ttyUSB1")
        self.running = False
        self.thread = threading.Thread(target=self.send)
        self.thread.daemon = True
        self.data_objList = []

    def start(self):
        try:
            self.RpmSensor.start()
            self.WindSpeedSensor.start()
            self.running = True
            self.thread.start()
        except Exception as ex:
            print(str(ex)) 

    def send(self):
        while True:
            if self.running:
                data_obj = self.get_current_data()
                with open("SystemData.txt", "a") as f:
                    f.write(str(data_obj) + "\n")

                self.data_objList.append(data_obj)
                try:
                    res = requests.post(
                        self.webAPI_url, json=self.data_objList)
                    if res.status_code == 200:
                        self.data_objList.clear()
                except requests.exceptions.RequestException as e:
                    print(e)

            time.sleep(self.interval)

    def get_current_data(self):
            # lat, lon = self.GPS.get_coordinates()
            # V_gen, I_gen = self.generator_meter.getReading()
            # V_inv, I_inv = self.inverter_meter.getReading()
            rpm = self.RpmSensor.get_rpm()
            windSpeed = self.WindSpeedSensor.get_wind_speed()
            dateTime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            data_obj = {
                "dateTime": dateTime,
                "voltage_generator": None,
                "current_generator": None,
                "voltage_inverter": None,
                "current_inverter": None,
                "rpm": rpm,
                "windSpeed": windSpeed,
                "latitude": None,
                "longitude": None
            }
            return data_obj
        
    def stop_sending(self):
        try:
            self.running = False
            return True
        except Exception as ex:
            return False
    
    def start_sending(self):
        try:
            self.running = True
            return True
        except Exception as ex:
            return False

    def change_interval(self, interval: float):
        try:
            self.interval = interval
            return True
        except Exception as ex:
            return False
