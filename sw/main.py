from Subsystems.motor import Motor, MotorArray
from Subsystems.servo import Servo
from machine import Pin, SoftI2C, I2C
from line_follower.DFRobot_SEN0017 import DFRobot_SEN0017
from line_follower.FollowerArray import FollowerArray
import line_to_junction

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
line_to_junction.drive_until_junction(motor_left,motor_right,left2,left1,right1,right2,50,1) 
line_to_junction.junction_turn(motor_left,motor_right,left2,left1,right1,right2,1)
line_to_junction.drive_until_junction(motor_left,motor_right,left2,left1,right1,right2,70,1)
line_to_junction.junction_turn(motor_left,motor_right,left2,left1,right1,right2,0)
line_to_junction.drive_until_junction(motor_left,motor_right,left2,left1,right1,right2,70,6)
line_to_junction.junction_turn(motor_left,motor_right,left2,left1,right1,right2,0)
line_to_junction.drive_until_junction(motor_left,motor_right,left2,left1,right1,right2,70,1)
line_to_junction.junction_turn(motor_left,motor_right,left2,left1,right1,right2,0)
line_to_junction.drive_until_junction(motor_left,motor_right,left2,left1,right1,right2,70,6)
line_to_junction.junction_turn(motor_left,motor_right,left2,left1,right1,right2,0)
line_to_junction.drive_until_junction(motor_left,motor_right,left2,left1,right1,right2,70,1)
line_to_junction.junction_turn(motor_left,motor_right,left2,left1,right1,right2,1)
line_to_junction.drive_until_junction(motor_left,motor_right,left2,left1,right1,right2,70,1)

print("main.py Done!")