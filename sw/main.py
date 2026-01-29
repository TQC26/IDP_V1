from Subsystems.motor import Motor
from Subsystems.servo import Servo
from machine import Pin, SoftI2C, I2C
from libs.tcs3472_micropython.tcs3472 import tcs3472

# Imports for testing - comment when done
from test_mfrc522 import test_mfrc522
from test_TMF8x01_get_distance import test_TMF8x01_get_distance
from test_STU_22L_IO_Mode import test_STU_22L_IO_Mode
from test_STU_22L_UART import test_STU_22L_UART
<<<<<<< HEAD
from machine import Pin, SoftI2C, I2C
from libs.tcs3472_micropython.tcs3472 import tcs3472
from libs.line_follower.DFRobot_SEN0017 import DFRobot_SEN0017


print("Welcome to main.py!")
=======
from sw.test_colour_sensor import test_tcs3472
from sw.test_ranging_sensor import test_vl53l0x
from test_led import test_led
from test_servo import test_pwn
from test_input import test_input_poll
from test_motor import test_motor3
>>>>>>> 56701a2f2b55da40192f3a1618183b1d7e316cc8

# Uncomment the test to run
# test_led()
# test_led_pwm()
# test_input_poll()
# test_motor3()
# test_tcs3472()
# test_actuator1()
# test_vl53l0x()
# test_mfrc522()
# test_TMF8x01_get_distance()
# test_STU_22L_IO_Mode()
# test_STU_22L_UART()
# test_tiny_code_reader()


# Plan for final code
State=0
# Init motors
motor_left = Motor(dirPin=2, PWMPin=3)
motor_right = Motor(dirPin=4, PWMPin=5)


# Init servos
servo1 = Servo(PWMPin=28)
servo2 = Servo(PWMPin=29)

#Init sensors
sens_pin = 22 # GPT22
left1 = DFRobot_SEN0017(sens_pin)

sens_pin = 23 # GPT23
left2 = DFRobot_SEN0017(sens_pin)

sens_pin = 24 # GPT22
right1 = DFRobot_SEN0017(sens_pin)

sens_pin = 25 # GPT22
right2 = DFRobot_SEN0017(sens_pin)

# State 0: Move front to leave starting box 
# State 1: No reel, line following until left sees white and turn left
# 
# Determine rack 
    ## if Upper rack:
        ###Line follow 


#State 1 --> State 2

#Line follow test
#Sensors left2, left1, right1, right2
Kp=5
Ki=0.0
Kd=0.0
integral=0
last_error=0
set_velocity=50

while True:
#Assuming no distractors, can adjust weight of 
    error=(left1-right1+2*(left2-right2))
    # if robot is too right, left sensor touches white line more, left1>right1, error>0
    # if robot is too left, right sensor touches white line more, left1<right1, error<0
    integral = error+integral
    output=error*Kp+integral*Ki+(error-last_error)*Kd
    last_error=error
<<<<<<< HEAD
    motor_left.Forward(min(-100,max(100,set_velocity-output)))
    motor_right.Forward(min(-100,max(100,set_velocity+output)))



# going from 9 - 31 heading north

# Dijkstra --> Get path sequence (Include turning angle) --> Detect Junctions (ie. we program each junction to have a determinncy test with the 4 sensors) 
# 0011 / 0111 --> There is a right junction
# 1100 / 1011 --> There is a left junction
# If require a turn --> Initiate a motor maneouver to turn 20 degrees (approx), and until the XX1X



print("main.py Done!")
=======
    motor_left.Forward(max(100,set_velocity-output))
    motor_right.Forward(max(100,set_velocity+output))
>>>>>>> 56701a2f2b55da40192f3a1618183b1d7e316cc8
