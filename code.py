from machine import idle, Pin, PWM
from time import sleep
import math

RPM = 79

class Servo:
    def __init__(self, pin, r=0):
        self.pin = pin
        self.pwm = PWM(Pin(self.pin))
        self.pwm.freq(50)
    def turn(self,angle):
        """
        turns the servo a given angle [INACCURATE]
        """
        angle *= 2
        # servo is continuous so we have to do this ourselves
        #for i
        if angle == 0: return
        ang_vel = 2 * math.pi * RPM / 60
        dt =  abs((angle) / ang_vel)
        print(dt)
        self.pwm.duty_u16(8000 if angle > 0  else 3000)
        sleep(dt)
        self.pwm.duty_u16(5000)
        
    def go(self, direction="ccw"):
        if direction == "cw":
            self.pwm.duty_u16(8000)
        elif direction == "ccw":
            self.pwm.duty_u16(3000)
        else:
            raise Exception("bad direction: only cw/ccw")
        
    def stop(self):
        self.pwm.duty_u16(5000)     
    
    def displace(self, distance):
        if self.r == 0:
            raise Exception("you should probably define `r` before calling this")
        angle = distance / self.r
        angle *= 2
        if angle == 0: return
        ang_vel = 2 * math.pi * RPM / 60
        dt =  abs((angle) / ang_vel)
        print(dt)
        self.pwm.duty_u16(8000 if angle > 0  else 3000)
        sleep(dt)
        self.pwm.duty_u16(5000)
        

servo = Servo(20)
servo.go()
sleep(10)
servo.stop()

while True:
    pass

