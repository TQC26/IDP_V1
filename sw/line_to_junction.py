import time
from Subsystems.motor import Motor
from Subsystems.servo import Servo
from machine import Pin, SoftI2C, I2C
from line_follower.DFRobot_SEN0017 import DFRobot_SEN0017

def drive_until_junction(motor_left,motor_right,left2,left1,right1,right2,speed=70):    
    # Constants
    Kp=5
    Ki=0.0
    Kd=0.0
    integral=0
    last_error=0
    
    print("Initiative move until junction...")
    
    while True:
        # Read Sensors
        # returns 1 for line, 0 for no line
        l2=left2.value()
        l1=left1.value()
        r1=right1.value()
        r2=right2.value()

        # Check Exit Condition (Junction)
        if (l2 and l1) or (r1 and r2):
            print("Stopping.")
            motor_left.off()
            motor_right.off()
            break

        error=(l1-r1)+3*(l2-r2)
        integral+=error
        derivative=error-last_error
        output=(error*Kp)+(integral*Ki)+(derivative*Kd)
        last_error = error

        # 5. Apply to Motors
        left_speed=max(-100, min(100,speed-output))
        right_speed=max(-100, min(100,speed+output))
        motor_left.Forward(left_speed)
        motor_right.Forward(right_speed)
        
        # Tiny sleep to stabilize reading
        time.sleep(0.002)