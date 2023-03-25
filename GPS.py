import serial
import time

class GPS:
    def __init__(self, port="/dev/ttyUSB2"):
        self.SIM7600X = serial.Serial(port,  115200, timeout=5)
        #self.SIM7600X.open()
        #Turn on GPS
        self.SIM7600X.write(b'AT+CGPS=1\r')
        self.SIM7600X.readlines()
    
    def get_coordinates(self):
        self.SIM7600X.write(b'AT+CGPSINFO\r')
        time.sleep(0.1)
        response = self.SIM7600X.readlines()
        for byte in response:
            str = byte.decode()
            if str.startswith('+'):
                return self.read_coordinates(str.split()[1])
        return None,None
        
    def read_coordinates(self,gpsStr):
        try:
            gpsInfoList = gpsStr.split(',')
            # Extract the latitude and longitude values
            lat_str, lat_dir, lon_str, lon_dir = gpsInfoList[:4]
            
            # Convert the latitude and longitude values to decimal degrees
            lat_dd = self.DMS_to_DD(float(lat_str))
            if lat_dir == 'S':
                lat_dd *= -1
            lon_dd = self.DMS_to_DD(float(lon_str))
            if lon_dir == 'W':
                lon_dd *= -1
            return lat_dd, lon_dd
        except Exception as ex:
            return None,None

    def DMS_to_DD(self, coord:float):
        return int(coord / 100) + coord % 100 / 60

#For testing
if __name__ == '__main__':
    # Create and start RPM sensor object
    gps = GPS()
    try:
        # Continuously print RPM readings
        while True:
            print(gps.read_coordinates("2221.783144,N,11406.841165,E,130323,210514.0,146.8,0.0,"))
            time.sleep(0.5)
    except KeyboardInterrupt:
        print('end')
        
        
#python -m serial.tools.list_ports -v