import time
import RPi.GPIO as GPIO

class ServoBlaster():
    def __init__(self, gpio_port=18):
        self._gpio_port = gpio_port
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._gpio_port, GPIO.OUT)
        self._pwm = GPIO.PWM(self._gpio_port, 50)
        self._pwm.start(0)

    def update(self, duty_cycle):
        self._pwm.ChangeDutyCycle(duty_cycle)

    def cleanup(self):
        self._pwm.stop()
        GPIO.cleanup()

class ServoAngle():
    def __init__(self, gpio_port, angle_min, angle_max, min_duty, max_duty):
        self._gpio_port = gpio_port
        self._angle_to_duty = (max_duty - min_duty) / (angle_max - angle_min)
        self._duty_min = min_duty
        self._angle_min = angle_min
        self._angle_max = angle_max

        self._angle = 0

        self._servo = ServoBlaster(self._gpio_port)

    def angle_to_duty(self, angle):
        duty = (angle - self._angle_min) * self._angle_to_duty + self._duty_min
        return duty

    def update(self, angle):
        duty_cycle = self.angle_to_duty(angle)
        self._servo.update(duty_cycle)

        self._angle = angle

    def set_to_min(self):
        self.update(self._angle_min)

    def set_to_max(self):
        self.update(self._angle_max)

    def set_to_middle(self):
        middle_angle = (self._angle_min + self._angle_max) * 0.5
        self.update(middle_angle)

    @property
    def angle(self):
        return self._angle

    @property
    def angle_min(self):
        return self._angle_min

    @property
    def angle_max(self):
        return self._angle_max


if __name__ == '__main__':
    servo_pin = 18
    servo_angle = ServoAngle(servo_pin, -85, 85, 2.5, 12.5)
