from Subsystems.motor import MOTOR_LEFT, MOTOR_RIGHT, Motor, MotorArray
from Subsystems.servo import Servo
from Subsystems.navigation import Location
import course_graph as crs
from machine import Pin, SoftI2C, I2C, ADC
from line_follower.FollowerArray import FollowerArray
import line_following
import line_to_junction
import resistance_checker
from libs.DFRobot_TMF8x01.DFRobot_TMF8x01 import DFRobot_TMF8701
from libs.VL53L0X.VL53L0X import VL53L0X
import time


# Init motors
motor_left = Motor(dirPin=7, PWMPin=6)
motor_right = Motor(dirPin=4, PWMPin=5)
mot_arr = MotorArray(motor_left, motor_right)

'''
# Init servos
servo1 = Servo(PWMPin=28)
servo2 = Servo(PWMPin=29)
'''

#Init resistance sensing
adc0 = machine.ADC(28) # ADC0 pin is GP26

#Init tracking sensors
left2 = 21
left1 = 22
right1 = 26
right2 = 27
sens_arr = FollowerArray([left2, left1, right1, right2])

'''
#Init ranging sensor
 # config I2C Bus
i2c_bus = I2C(id=0, sda=Pin(19), scl=Pin(20))
# Setup vl53l0 object
ranging_sens = VL53L0X(i2c_bus)
ranging_sens.set_Vcsel_pulse_period(ranging_sens.vcsel_period_type[0], 18)
ranging_sens.set_Vcsel_pulse_period(ranging_sens.vcsel_period_type[1], 14)
ranging_sens.start()

#Init ToF sensor
# config I2C Bus
i2c_bus = I2C(id=0, sda=Pin(17), scl=Pin(18), freq=100000) 
tof_sens = DFRobot_TMF8701(i2c_bus=i2c_bus)
while(tof_sens.begin() != 0):
    time.sleep(0.5)
tof_sens.start_measurement(calib_m = tof_sens.eMODE_NO_CALIB, mode = tof_sens.eCOMBINE) #change to ePROXIMITY / eDISTANCE if needed

'''

'''#Line Following Test
line_following.line_following_test(mot_arr,sens_arr)
'''

'''
#Starting Position
line_to_junction.drive_until_junction(mot_arr, sens_arr,90,skip=0)
'''
# Pathfinding test
# Init navigation
location = Location(35, mot_arr, sens_arr, crs.course)

from test_files.test_pathfinding import pathfinding_test
pathfinding_test(location)


line_to_junction.junction_placement(mot_arr,sens_arr,50)

'''
Go forward till junction (35)
35-->37
Intake Seq & 180 turn
37--> Wherever it detects
Junction Seq
-->36
Intake Seq & 180 turn
36--> Wherever it detects
Junction Seq
Intake Seq & 180 turn
38--> Wherever it detects
Junction Seq
Intake Seq & 180 turn
39--> Wherever it detects
Junction Seq
'''