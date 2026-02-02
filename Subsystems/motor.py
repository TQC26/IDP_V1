from machine import Pin, PWM
from utime import sleep

SPIN_ANGSPEED = 15

'''An array of drive motors which can be used for steering'''
class MotorArray:
    def __init__(self, motLeft, motRight):
        self.motors = [motLeft, motRight]
        self.heading = 0

    def forward(self, speed=100):
        for motor in motors:
            motor.forward(speed)
    
    def reverse(self, speed=100):
        for motor in motors:
            motor.reverse(speed)
            
    '''Come to a full stop then spin on the spot by approx. delta degrees'''
    def spin(self, delta=90):
        if delta == 0:
            return
        self.heading += delta

        # Inside motor is initially set to RHS motor
        imot_inside = 1
        if delta < 0:
            mot_inside = 0
        
        mot_inside = self.motors[imot_inside]
        mot_outside = self.motors[len(self.motors) - imot_inside]
        
        mot_inside.off()
        mot_outside.off()
        
        mot_inside.reverse(100)
        mot_outside.forward(100)
        
        delta_abs = delta
        if delta_abs < 0:
            delta_abs *= -1
        
        # Time here tuned by SPIN_ANGSPEED
        sleep(delta_abs / SPIN_ANGSPEED)
        
    '''Corner by adjusting the inside motor's speed without changing the outside.
    Creates a smooth cornering manouver'''
    def corner(self, delta=90):
        # TODO: Proper cornering code here
        self.spin(delta)
        
    def get_heading(self):
        return self.heading
        
class Motor:
    def __init__(self, dirPin, PWMPin):
        self.mDir = Pin(dirPin, Pin.OUT)  # set motor direction pin
        self.pwm = PWM(Pin(PWMPin))  # set motor pwm pin
        self.pwm.freq(1000)  # set PWM frequency
        self.pwm.duty_u16(0)  # set duty cycle - 0=off
        
    def off(self):
        self.pwm.duty_u16(0)
        
    def forward(self, speed=100):
        if(speed<0): self.Reverse(speed*-1)
        else:   
            self.mDir.value(0)                     # forward = 0 reverse = 1 motor
            self.pwm.duty_u16(int(65535 * speed / 100))  # speed range 0-100 motor

    def reverse(self, speed=30):
        if(speed<0): self.Forward(speed*-1)
        else:
            self.mDir.value(1)
            self.pwm.duty_u16(int(65535 * speed / 100))