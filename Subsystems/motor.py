from machine import Pin, PWM
from utime import sleep

SPIN_ANGSPEED = 15

MOTOR_LEFT = 0
MOTOR_RIGHT = 1

'''An array of drive motors which can be used for steering'''
class MotorArray:
    def __init__(self, motLeft, motRight):
        self.motors = [motLeft, motRight]
            
    '''Adjust speed for the specified motor to the given value.
    Speed value can be in the range [-100 100], with negative values initiating a reverse.
    '''
    def tank(self,newSpeed_left,newSpeed_right):
            self.motors[0].forward(newSpeed_left)
            self.motors[1].forward(newSpeed_right)
            
    def off(self):
            self.motors[0].off()
            self.motors[1].off()
            
    '''Come to a full stop then spin on the spot. Direction determines the inside motor.'''
    def spin(self, direction=MOTOR_LEFT):
        if direction==MOTOR_LEFT:
            self.tank(-65,100)
        else:
            self.tank(100,-65)

    '''Corner by adjusting the inside motor's speed without changing the outside.
    Creates a smooth cornering manouver'''
    def turn(self, direction=MOTOR_LEFT):
        if direction==MOTOR_LEFT:
            self.tank(25,100)
        else:
            self.tank(100,25)
        
    def corner(self, direction=MOTOR_LEFT, bay=False):
        if bay:
            self.spin(direction)
        else:
            self.turn(direction)
        
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
        if(speed<0): self.reverse(speed*-1)
        else:   
            self.mDir.value(0)                     # forward = 0 reverse = 1 motor
            self.pwm.duty_u16(int(65535 * speed / 100))  # speed range 0-100 motor

    def reverse(self, speed=30):
        if(speed<0): self.forward(speed*-1)
        else:
            self.mDir.value(1)
            self.pwm.duty_u16(int(65535 * speed / 100))
