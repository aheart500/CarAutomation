import Servo as sb
import TFMini
import time
import math

class TfminiServoScanner():
    def __init__(self, servo_gpio=18, angle_min=-90, angle_max=90, duty_min=2.5, duty_max=12.5, n_steps=10, serial_port= '/dev/ttyS0', time_min_max=0.5):
        self.servo = sb.ServoAngle(servo_gpio, angle_min, angle_max, duty_min, duty_max)
        self.laser = TFMini.TFMini(serial_port)

        self._delta_angle = 5
        self._time_min_max = time_min_max
        self._servo_speed = (angle_max -angle_min)/ time_min_max

        self._min_time_sleep = self._delta_angle/self._servo_speed

        self._move_dir = 1
     
    def read_laser(self):
        return(self.laser.get_data())
        
    def reset_servo(self):
        self.servo.set_to_min()
        self._move_dir = 1
        time.sleep(self._time_min_max)

    def move_servo(self):
        angle = self.angle

        if angle >= self.servo.angle_max - self._delta_angle:
            self._move_dir =-1
        if angle <= self.servo.angle_min + self._delta_angle:
            self._move_dir =1
        
        angle += self._delta_angle * self._move_dir
        self.servo.update(angle)

        time.sleep(self._min_time_sleep)

    def scan(self, scale_factor=1.0, reset=False):
        if reset: self.reset_servo()

        ini_angle = self.angle
        self.servo.update(ini_angle)

        ranges =[]
        angle = ini_angle
        move_dir = self._move_dir
        time_init = time.time()
        while True:
            dist = self.read_laser()*scale_factor
            angle = self.angle
            print("d - %4f  a= %4f"%(dist,self.angle))
            ranges.append(dist)
            self.move_servo()

            if move_dir*self._move_dir <0:
                break
        
        time_increment = (time.time() - time_init)/(len(ranges)-1)
        angle_increment = (angle-ini_angle)/(len(ranges)-1)

        return(ini_angle, angle, time_increment, angle_increment, ranges)
    @property
    def angle(self):
        return(self.servo.angle)

if __name__ == "__main__":
    pass
    
