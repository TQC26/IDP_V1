from Subsystems.motor import MOTOR_LEFT, MOTOR_RIGHT, Motor, MotorArray
from Subsystems.servo import Servo
from Subsystems.navigation import Location
import course_graph as crs
from machine import Pin, SoftI2C, I2C, ADC
from line_follower.FollowerArray import FollowerArray
import line_following
import line_to_junction
import junction_sequence
import resistance_checker
from libs.DFRobot_TMF8x01.DFRobot_TMF8x01 import DFRobot_TMF8701
from libs.VL53L0X.VL53L0X import VL53L0X
import time

# Print banner
print("Starting IDP robot software")
print("Dedicated to the memories of Ethan, Ernest, Nathan, Arielle, Peter and Michael")

# Init motors
motor_left = Motor(dirPin=7, PWMPin=6)
motor_right = Motor(dirPin=4, PWMPin=5)
mot_arr = MotorArray(motor_left, motor_right)

# Init servos
servo1 = Servo(Pin(13))
servo2 = Servo(Pin(15))
servo1.goto(0)
servo2.goto(120)

# Init resistance sensing
adc0 = machine.ADC(28) # ADC0 pin is GP26

# Init tracking sensors
left2 = 21
left1 = 22
right1 = 26
right2 = 27
sens_arr = FollowerArray([left2, left1, right1, right2])

# IMPORTANT NOTE: Do not change distance sensors to hardware I2C!
# The sensors (due to a soldering issue) are spanning busses, which is not supported by
# hardware I2C.

# Init ranging sensor
# config I2C Bus
i2c_bus = SoftI2C(sda=Pin(20), scl=Pin(19))
# Setup vl53l0 object
ranging_sens = VL53L0X(i2c_bus)
ranging_sens.set_Vcsel_pulse_period(ranging_sens.vcsel_period_type[0], 18)
ranging_sens.set_Vcsel_pulse_period(ranging_sens.vcsel_period_type[1], 14)
ranging_sens.start()

# Init ToF sensor
# config I2C Bus
i2c_bus = SoftI2C(sda=Pin(18), scl=Pin(17), freq=100000)
tof_sens = DFRobot_TMF8701(i2c_bus=i2c_bus)
while(tof_sens.begin() != 0):
    time.sleep(0.5)
tof_sens.start_measurement(calib_m = tof_sens.eMODE_NO_CALIB, mode = tof_sens.eDISTANCE) #change to ePROXIMITY / eDISTANCE if needed

# Init LEDs
led_pin1 = 9
led_pin2 = 8
led_pin3 = 10
led_pin4 = 11
led1 = Pin(led_pin1, Pin.OUT)
led2 = Pin(led_pin2, Pin.OUT)
led3 = Pin(led_pin3, Pin.OUT)
led4 = Pin(led_pin4, Pin.OUT)
led_array=[led1,led2,led3,led4]
# Init navigation
location = Location(35, mot_arr, sens_arr, crs.course)

# Initial position
line_to_junction.drive_until_junction(mot_arr, sens_arr, speed=95)

# Set servos
servo_arr=[servo1,servo2]
servo_arr[0].goto(40)
servo_arr[1].goto(60)

intake_sequence=[36,37,38,39,36,37,38,39]
# Drive to first intake box
for i in intake_sequence:
    location.drive_to_node(i, speed=95)
    line_to_junction.line_alignment(mot_arr,sens_arr)
    line_to_junction.intake(mot_arr,servo_arr)
    # Force turning CCW if on a node too close to the bench edge
    line_to_junction.leave_intake(mot_arr,sens_arr, forceDirection = (i == 37))
    location.heading=0
    destination=resistance_checker.reel_type_to_node(adc0,led_array)
    location.drive_to_node(destination,speed=95)
    if destination==17:
        rack=3
    elif destination==24:
        rack=2
    elif destination==23:
        rack=1
    else:
        rack=0
    junction_sequence.junction_sequence(mot_arr,sens_arr,servo_arr,ranging_sens,tof_sens,led_array,rack)
    location.heading=180

navigation.drive_to_node(start_point, speed=90)
