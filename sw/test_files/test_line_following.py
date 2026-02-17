from Subsystems.motor import MOTOR_LEFT, MOTOR_RIGHT, Motor, MotorArray
from Subsystems.servo import Servo
from machine import Pin, SoftI2C, I2C
from line_follower.DFRobot_SEN0017 import DFRobot_SEN0017
from line_follower.FollowerArray import FollowerArray
import line_to_junction
import time

def line_following_test(mot_arr,sens_arr):

    #Leaving Starting Position
    line_to_junction.drive_until_junction(mot_arr,sens_arr,95,1) 
    line_to_junction.junction_turn(mot_arr,sens_arr,1)
    line_to_junction.drive_until_junction(mot_arr,sens_arr,95,1)
    line_to_junction.junction_turn(mot_arr,sens_arr,0)
    line_to_junction.drive_until_junction(mot_arr,sens_arr,95,6)
    line_to_junction.junction_turn(mot_arr,sens_arr,0)
    line_to_junction.drive_until_junction(mot_arr,sens_arr,95,1)
    line_to_junction.junction_turn(mot_arr,sens_arr,0)
    line_to_junction.drive_until_junction(mot_arr,sens_arr,95,6)
    line_to_junction.junction_turn(mot_arr,sens_arr,0)
    line_to_junction.drive_until_junction(mot_arr,sens_arr,95,1)

    #Heading back into the junction
    mot_arr.corner(MOTOR_RIGHT)
    time.sleep(1.8)
    line_to_junction.drive_until_junction(mot_arr,sens_arr,95,0)
    mot_arr.off()