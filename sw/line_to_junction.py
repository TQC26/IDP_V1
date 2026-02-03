import time
from Subsystems.motor import Motor, MOTOR_LEFT, MOTOR_RIGHT
from Subsystems.servo import Servo
from machine import Pin, SoftI2C, I2C
from line_follower.DFRobot_SEN0017 import DFRobot_SEN0017
from line_follower.FollowerArray import JUNCTION_TYPE_NONE

button_pin = 16
button = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)

def hardstop(motor_array):
    if button.value()==1:
        motor_array.off()
        time.sleep(100)

def drive_until_junction(motor_array, sensor_array,speed=40,skip=0):    #motor_left,motor_right,left2,left1,right1,right2
    # Constants
    Kp=10
    Ki=0.01
    Kd=0.01
    integral=0
    last_error=0
    
    print("Initiative move until junction...")
    
    while True:
        # Poll Sensor Array
        hardstop(motor_array)
        junction = sensor_array.detect_junction()

        # Check Exit Condition (Junction)
        if junction != JUNCTION_TYPE_NONE:
            motor_array.off()
            if skip>0:
                #time.sleep(1) #Testing purposes
                junction_turn(motor_array,sensor_array,turn_mode=2)
                #time.sleep(1) #Testing purposes
                skip-=1
            else:
                print("Stopping.")
                #time.sleep(1) #Testing purposes
                return junction
        l2=sensor_array.array[0].on_line()
        l1=sensor_array.array[1].on_line()
        r1=sensor_array.array[2].on_line()
        r2=sensor_array.array[3].on_line()
        error=(l1-r1)+8*(l2-r2)
        integral+=error
        derivative=error-last_error
        output=(error*Kp)+(integral*Ki)+(derivative*Kd)
        last_error = error

        # 5. Apply to Motors
        print(max(-100, min(100,speed-output)),max(-100, min(100,speed+output)))
        left_speed=max(-100, min(100,speed-output))
        right_speed=max(-100, min(100,speed+output))
        motor_array.tank(left_speed,right_speed)
        
        # Tiny sleep to stabilize reading
        time.sleep(0.002)
        
def junction_turn(motor_array,sensor_array,turn_mode=0): #0 = turn left, 1 = turn right, 2=straight
    print("turning")
    if turn_mode==0:
        while True:
            hardstop(motor_array)
            r1=sensor_array.array[2].on_line()
            l1=sensor_array.array[1].on_line()
            if r1==0 and l1==0:
                break
            motor_array.corner(MOTOR_LEFT)
            time.sleep(0.002)
            
        while True:
            hardstop(motor_array)
            r1=sensor_array.array[2].on_line()
            if r1==1:
                break
            motor_array.corner(MOTOR_LEFT)
            time.sleep(0.002)
            
        motor_array.off()
    
    elif turn_mode==1:
        while True:
            hardstop(motor_array)
            r1=sensor_array.array[2].on_line()
            l1=sensor_array.array[1].on_line()
            if r1==0 and l1==0:
                break
            motor_array.corner(MOTOR_RIGHT)
            time.sleep(0.002)
            
        while True:
            hardstop(motor_array)
            l1=sensor_array.array[1].on_line()
            if l1==1:
                break
            motor_array.corner(MOTOR_RIGHT)
            time.sleep(0.002)

        motor_array.off()
        
    else:
        motor_array.tank(70,70)
        time.sleep(0.5)
        motor_array.off()