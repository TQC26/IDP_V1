from Subsystems.motor import MOTOR_LEFT, MOTOR_RIGHT, Motor, MotorArray
from Subsystems.servo import Servo
from machine import Pin, SoftI2C, I2C
from line_follower.DFRobot_SEN0017 import DFRobot_SEN0017
from line_follower.FollowerArray import FollowerArray
import line_to_junction
import time

State=0

# Init motors
motor_left = Motor(dirPin=7, PWMPin=6)
motor_right = Motor(dirPin=4, PWMPin=5)

mot_arr = MotorArray(motor_left, motor_right)

# Init servos
#servo1 = Servo(PWMPin=28)
#servo2 = Servo(PWMPin=29)

#Init sensor
left2 = DFRobot_SEN0017(21)
left1 = DFRobot_SEN0017(22)
right1 = DFRobot_SEN0017(26)
right2 = DFRobot_SEN0017(27)


sens_arr = FollowerArray([left2, left1, right1, right2])

#Leaving Starting Position

line_to_junction.drive_until_junction(mot_arr,sens_arr,50,1) 
line_to_junction.junction_turn(mot_arr,sens_arr,1)
line_to_junction.drive_until_junction(mot_arr,sens_arr,90,1)
line_to_junction.junction_turn(mot_arr,sens_arr,0)
line_to_junction.drive_until_junction(mot_arr,sens_arr,90,6)
line_to_junction.junction_turn(mot_arr,sens_arr,0)
line_to_junction.drive_until_junction(mot_arr,sens_arr,90,1)
line_to_junction.junction_turn(mot_arr,sens_arr,0)
line_to_junction.drive_until_junction(mot_arr,sens_arr,90,6)
line_to_junction.junction_turn(mot_arr,sens_arr,0)
line_to_junction.drive_until_junction(mot_arr,sens_arr,90,1)

mot_arr.corner(MOTOR_RIGHT)
time.sleep(1.4)
line_to_junction.drive_until_junction(mot_arr,sens_arr,80,0)
mot_arr.off()
print("main.py Done!")