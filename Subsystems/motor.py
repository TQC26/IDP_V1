from machine import Pin, PWM
from utime import sleep

SPIN_ANGSPEED = 15

MOTOR_LEFT = 0
MOTOR_RIGHT = 1

'''An array of drive motors which can be used for steering'''
class MotorArray:
    def __init__(self, motLeft, motRight):
        self.motors = [motLeft, motRight]
        
    '''Returns a tuple (motor_inside, motor_outside)'''
    def _select_inside(self, direction):
        mot_inside = self.motors[0]
        mot_outside = self.motors[1]
        if direction == MOTOR_RIGHT:
            mot_inside = self.motors[1]
            mot_outside = self.motors[0]
            
        return (mot_inside, mot_outside)

    def forward(self, speed=100):
        for motor in motors:
            motor.forward(speed)
    
    def reverse(self, speed=100):
        for motor in motors:
            motor.reverse(speed)
            
    '''Adjust speed for the specified motor to the given value.
    Speed value can be in the range [-100 100], with negative values initiating a reverse.
    '''
    def adjust_speed(self, mot, newSpeed):
        if newSpeed >= 0:
            self.motors[mot].forward(newSpeed)
        else:
            self.motors[mot].reverse(abs(newSpeed))
            
    '''Come to a full stop then spin on the spot. Direction determines the inside motor.'''
    def spin(self, direction=MOTOR_LEFT):
        for motor in self.motors:
            motor.off()
            
        mots = self._select_inside()
        mot_inside = mots[0]
        mot_outside = mots[1]
        
        mot_inside.reverse(100)
        mot_outside.forward(100)
        
    '''Corner by adjusting the inside motor's speed without changing the outside.
    Creates a smooth cornering manouver'''
    def corner(self, direction=MOTOR_LEFT):
        mots = self._select_inside()
        mot_inside = mots[0]
        mot_outside = mots[1]
        
        mot_inside.reverse(50)
        mot_outside.forward(100)
        
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