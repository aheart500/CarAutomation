import serial
class TFMini():
    def __init__(self, serial_port='/dev/ttyS0'):
        self._ser= serial.Serial(serial_port,115200)
        if self._ser.is_open == False:
            self._ser.open()
        self._distance = 0

    def get_data(self):
        while True:
            distance = -1
            recv = self._ser.read(9)
            if len(recv) > 4:
                self._ser.reset_input_buffer()
                if recv[0] == 0x59 and recv[1] == 0x59: 
                    low = recv[2]
                    high = recv[3]
                    distance = low + high * 256
                    break
        self._distance = distance
        return(distance)
    @property
    def distance(self):
        return(self._distance)
    
    def print_data_thread(self):
        while True:
            currentDistance = self.get_data()
            if currentDistance > -1:
                print(currentDistance)
    
    def close(self):
        if self._ != None:
            self._ser.close()
if __name__ == '__main__':
    tfmin = TFMini()
    tfmin.print_data_thread()