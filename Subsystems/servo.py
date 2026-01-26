from machine import Pin, PWM

class Servo:
    def __init__(self, pin_num):
        self.pwn = PWM(Pin(pin_num), 100)
        self.direction = 1  # 1=up, -1=down
        self.level = 0
        self.max_angle = 270

    def goto(self, angle):
        if angle < 0: angle = 0
        if angle > self.max_angle: angle = self.max_angle
        
        self.level=angle
       
        u16_level = int(65535 * self.level / 100)
        self.duty_u16(u16_level)
 
    def off(self):
        self.pwm.duty_u16(0)