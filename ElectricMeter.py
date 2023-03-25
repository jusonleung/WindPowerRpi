import serial
import time

class ElectricMeter:
    def __init__(self, port="/dev/ttyUSB0"):
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = 2400
        self.ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
        self.ser.parity = serial.PARITY_EVEN  # set parity check
        self.ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
        self.ser.timeout = 1  # non-block read 0.5s
        try: 
            self.ser.open()
        except Exception as ex:
            print ("open serial port error " + str(ex))
            exit()
            
    def getReading(self):
        if self.ser.isOpen():
            try:
                self.ser.flushInput() #flush input buffer
                self.ser.flushOutput() #flush output buffer
        
                #get voltage
                self.ser.write(0x25)
                time.sleep(0.2)
                response = self.ser.read(2)
                voltage = int.from_bytes(response)
                
                #get current
                self.ser.write(0x2B)
                time.sleep(0.2)
                response = self.ser.read(2)
                current = int.from_bytes(response)
                
                return voltage,current
            except Exception as e1:
                print ("communicating error " + str(e1))
        else:
            print ("open serial port error")