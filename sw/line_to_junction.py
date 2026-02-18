import time
from Subsystems.motor import Motor, MOTOR_LEFT, MOTOR_RIGHT
from Subsystems.servo import Servo
from machine import Pin, SoftI2C, I2C
from line_follower.DFRobot_SEN0017 import DFRobot_SEN0017
from line_follower.FollowerArray import JUNCTION_TYPE_LEFT, JUNCTION_TYPE_NONE, JUNCTION_TYPE_RIGHT

JUNCTION_TIMEOUT_CONSTANT = 75

button_pin = 16
button = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)

def hardstop(motor_array):
    if button.value()==1:
        motor_array.off()
        time.sleep(100)

def intake(motor_array,servo_array):
    servo_array[1].goto(110)
    servo_array[0].goto(50)
    motor_array.tank(50,50)
    time.sleep(2)
    motor_array.tank(20,20)
    time.sleep(0.5)
    servo_array[1].goto(30)
    time.sleep(1)

    # Raise arm with forced slowness
    for i in range(50, 20, -1):
        servo_array[0].goto(i)
        time.sleep(0.02)

'''If ForceDirection is True, the bot will turn CCW'''
def leave_intake(motor_array, sensor_array, forceDirection=False):
    motor_array.tank(40, 40)
    time.sleep(1)
    if forceDirection:
        motor_array.tank(-80, 80)
    else:
        motor_array.tank(80,-80)
    time.sleep(1.0)
    
    if forceDirection:
        junction_turn(motor_array,sensor_array,turn_mode=0, bay=True)
    else:
        junction_turn(motor_array,sensor_array,turn_mode=1, bay=True)
    
    '''True
    while True:
        hardstop(motor_array)
        motor_array.tank(50,50)
        l2=sensor_array.array[0].on_line()
        l1=sensor_array.array[1].on_line()
        r1=sensor_array.array[2].on_line()
        r2=sensor_array.array[3].on_line()
        if l1+l2+r1+r2>0:
            break
    '''
    #line_alignment(motor_array, sensor_array)
    

def junction_alignment(motor_array, sensor_array):    #motor_left,motor_right,left2,left1,right1,right2
    Kp=50
    Ki=0.15
    Kd=0.05
    integral=0
    last_error=0
    speed=40
    
    print("Initiative move until junction...")
    blank_cnt=0
    while True:
        # Poll Sensor Array
        hardstop(motor_array)
        l2=sensor_array.array[0].on_line()
        l1=sensor_array.array[1].on_line()
        r1=sensor_array.array[2].on_line()
        r2=sensor_array.array[3].on_line()
        if l1+l2+r1+r2>0:
            blank_cnt=0
        else:
            blank_cnt+=1
        if blank_cnt>500:
            break
        error=(l1-r1)+0*(l2-r2)
        integral+=error
        derivative=error-last_error
        output=(error*Kp)+(integral*Ki)+(derivative*Kd)
        last_error = error

        # 5. Apply to Motors
        # print(max(-100, min(100,speed-output)),max(-100, min(100,speed+output)))
        left_speed=max(-100, min(100,speed-output))
        right_speed=max(-100, min(100,speed+output))
        motor_array.tank(left_speed,right_speed)
        
        # Tiny sleep to stabilize reading
        time.sleep(0.002)

def offload(motor_array, servo_array):
    motor_array.tank(60, 60)
    time.sleep(1)
    for _ in range(0, 2):
        motor_array.spin(MOTOR_LEFT)
        time.sleep(0.1)
        motor_array.spin(MOTOR_RIGHT)
        time.sleep(0.1)
    motor_array.tank(60, 60)
    time.sleep(1)
    servo_array[0].goto(30)
    servo_array[1].goto(70)
    motor_array.tank(-50, -50)
    time.sleep(1.2)
    
    
def line_alignment(motor_array, sensor_array):    #motor_left,motor_right,left2,left1,right1,right2
    # Constants
    Kp=20
    Ki=0.05
    Kd=0.05
    integral=0
    last_error=0
    speed=10
    
    print("Aligning to line")
    
    for i in range(500):
        # Poll Sensor Array
        hardstop(motor_array)
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
        # print(max(-100, min(100,speed-output)),max(-100, min(100,speed+output)))
        left_speed=max(-100, min(100,speed-output))
        right_speed=max(-100, min(100,speed+output))
        motor_array.tank(left_speed,right_speed)
        
        # Tiny sleep to stabilize reading
        time.sleep(0.002)

def junction_leave(motor_array, sensor_array,rack):    #motor_left,motor_right,left2,left1,right1,right2
    # Constants
    Kp=20
    Ki=0.05
    Kd=0.05
    integral=0
    last_error=0
    speed=-70
    
    print("Initiative move until junction...")
    
    for i in range (0,110):
        # Poll Sensor Array
        l2=sensor_array.array[0].on_line()
        l1=sensor_array.array[1].on_line()
        r1=sensor_array.array[2].on_line()
        r2=sensor_array.array[3].on_line()
        error=(l1-r1)+4*(l2-r2)
        integral+=error
        derivative=error-last_error
        output=(error*Kp)+(integral*Ki)+(derivative*Kd)
        last_error = error

        # 5. Apply to Motors
        # print(max(-100, min(100,speed+output)),max(-100, min(100,speed-output)))
        left_speed=max(-100, min(100,speed+output))
        right_speed=max(-100, min(100,speed-output))
        motor_array.tank(left_speed,right_speed)
        
        # Tiny sleep to stabilize reading
        time.sleep(0.002)
    if rack%2==0:
        motor_array.tank(60, -80)
        time.sleep(2)
        junction_turn(motor_array,sensor_array,turn_mode=0,bay=False)
    else:
        motor_array.tank(-80, 60)
        time.sleep(2)
        junction_turn(motor_array,sensor_array,turn_mode=1,bay=False)
    

def drive_until_junction(motor_array, sensor_array,speed=40,skip=0):    #motor_left,motor_right,left2,left1,right1,right2
    # Constants
    Kp=20
    Ki=0.05
    Kd=0.05
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
        error=(l1-r1)+1*(l2-r2)
        integral+=error
        derivative=error-last_error
        output=(error*Kp)+(integral*Ki)+(derivative*Kd)
        last_error = error

        # 5. Apply to Motors
        # print(max(-100, min(100,speed-output)),max(-100, min(100,speed+output)))
        left_speed=max(-100, min(100,speed-output))
        right_speed=max(-100, min(100,speed+output))
        motor_array.tank(left_speed,right_speed)
        
        # Tiny sleep to stabilize reading
        time.sleep(0.002)
        
#DO NOT EDIT     
def drive_leave_junction(motor_array,sensor_array,speed=40):  
    # Constants
    Kp=20
    Ki=0.05
    Kd=0.05
    integral=0
    last_error=0

    junction_countdown = 0
    
    while True:
        # Poll Sensor Array
        hardstop(motor_array)
        junction = sensor_array.detect_junction()

        sensor_overide=[0,0,0,0]
        # Check Exit Condition (Junction)
        if junction == JUNCTION_TYPE_NONE:
            motor_array.off()
            print("Stopping.")
            return junction
        elif junction == JUNCTION_TYPE_LEFT:
            sensor_overide[2]=1
            sensor_overide[3]=1
            junction_countdown = JUNCTION_TIMEOUT_CONSTANT
        elif junction == JUNCTION_TYPE_RIGHT:
            sensor_overide[1]=1
            sensor_overide[0]=1
            junction_countdown = JUNCTION_TIMEOUT_CONSTANT

        if junction_countdown == 0:
            l2=sensor_array.array[0].on_line()*sensor_overide[0]
            l1=sensor_array.array[1].on_line()*sensor_overide[1]
            r1=sensor_array.array[2].on_line()*sensor_overide[2]
            r2=sensor_array.array[3].on_line()*sensor_overide[3]
            error=(l1-r1)+8*(l2-r2)
            integral+=error
            derivative=error-last_error
            output=(error*Kp)+(integral*Ki)+(derivative*Kd)
            last_error = error
        else:
            junction_countdown -= 1
            output = 0

        # 5. Apply to Motors
        # print(max(-100, min(100,speed-output)),max(-100, min(100,speed+output)))
        left_speed=max(-100, min(100,speed+output))
        right_speed=max(-100, min(100,speed-output))
        motor_array.tank(left_speed,right_speed)
        
        # Tiny sleep to stabilize reading
        time.sleep(0.002)
    
#Turning at junctions
def junction_turn(motor_array,sensor_array,turn_mode=0, bay=False): #0 = turn left, 1 = turn right, 2=straight
    print("turning")
    if turn_mode==0:
        if bay:
            motor_array.corner(MOTOR_LEFT, bay)
            time.sleep(0.2)
            motor_array.off()
        while True:
            hardstop(motor_array)
            r1=sensor_array.array[2].on_line()
            l1=sensor_array.array[1].on_line()
            if r1==0 and l1==0:
                break
            motor_array.corner(MOTOR_LEFT, bay)
            time.sleep(0.002)
            
        while True:
            hardstop(motor_array)
            r1=sensor_array.array[2].on_line()
            if r1==1:
                break
            motor_array.corner(MOTOR_LEFT, bay)
            time.sleep(0.002)
            
        motor_array.off()
    
    elif turn_mode==1:
        if bay:
            motor_array.corner(MOTOR_RIGHT, bay)
            time.sleep(0.2)
            motor_array.off()
            
        while True:
            hardstop(motor_array)
            r1=sensor_array.array[2].on_line()
            l1=sensor_array.array[1].on_line()
            if r1==0 and l1==0:
                break
            motor_array.corner(MOTOR_RIGHT, bay)
            time.sleep(0.002)
            
        while True:
            hardstop(motor_array)
            l1=sensor_array.array[1].on_line()
            if l1==1:
                break
            motor_array.corner(MOTOR_RIGHT, bay)
            time.sleep(0.002)

        motor_array.off()
        
    else:
        drive_leave_junction(motor_array,sensor_array,95)
        motor_array.off()
