import time
from Subsystems.motor import Motor
from Subsystems.servo import Servo
from machine import Pin, SoftI2C, I2C
from line_follower.DFRobot_SEN0017 import DFRobot_SEN0017

def drive_until_junction(motor_left,motor_right,left2,left1,right1,right2,speed=40,skip=0):    
    # Constants
    Kp=10
    Ki=0.01
    Kd=0.01
    integral=0
    last_error=0
    
    print("Initiative move until junction...")
    
    while True:
        # Read Sensors
        # returns 1 for line, 0 for no line
        l2=left2.on_line()
        l1=left1.on_line()
        r1=right1.on_line()
        r2=right2.on_line()

        # Check Exit Condition (Junction)
        if (l2 and l1) or (r1 and r2):
            motor_left.off()
            motor_right.off()
            if skip>0:
                time.sleep(1) #Testing purposes
                junction_turn(motor_left,motor_right,left2,left1,right1,right2,turn_mode=2)
                time.sleep(1) #Testing purposes
                skip-=1
            else:
                print("Stopping.")
                time.sleep(1) #Testing purposes
                break

        error=(l1-r1)+8*(l2-r2)
        integral+=error
        derivative=error-last_error
        output=(error*Kp)+(integral*Ki)+(derivative*Kd)
        last_error = error

        # 5. Apply to Motors
        print(max(-100, min(100,speed-output)),max(-100, min(100,speed+output)))
        left_speed=max(-100, min(100,speed-output))
        right_speed=max(-100, min(100,speed+output))
        motor_left.Forward(left_speed)
        motor_right.Forward(right_speed)
        
        # Tiny sleep to stabilize reading
        time.sleep(0.002)
        
def junction_turn(motor_left,motor_right,left2,left1,right1,right2,turn_mode=0): #0 = turn left, 1 = turn right, 2=straight
    print("turning")
    if turn_mode==0:
        while True:
            r1=right1.on_line()
            if r1==0:
                break
            motor_left.Reverse(50)
            motor_right.Forward(100)
            time.sleep(0.002)
            
        while True:
            r1=right1.on_line()
            if r1==1:
                break
            motor_left.Reverse(50)
            motor_right.Forward(100)
            time.sleep(0.002)
            
        motor_left.off()
        motor_right.off()
    
    elif turn_mode==1:
        while True:
            l1=left1.on_line()
            if l1==0:
                break
            motor_right.Reverse(50)
            motor_left.Forward(100)
            time.sleep(0.002)
            
        while True:
            l1=left1.on_line()
            if l1==1:
                break
            motor_right.Reverse(50)
            motor_left.Forward(100)
            time.sleep(0.002)
            
        motor_left.off()
        motor_right.off()
    else:
        motor_left.Forward(50)
        motor_right.Forward(50)
        time.sleep(0.4)
        motor_left.off()
        motor_right.off()