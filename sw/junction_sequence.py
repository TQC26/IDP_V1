from Subsystems.motor import MOTOR_LEFT, MOTOR_RIGHT, Motor, MotorArray
from Subsystems.servo import Servo
from machine import Pin, SoftI2C, I2C
from line_follower.DFRobot_SEN0017 import DFRobot_SEN0017
from line_follower.FollowerArray import FollowerArray
import line_to_junction
import time

ToF_box_constant=220
Ranging_box_constant=220

def junction_sequence(mot_arr,sens_arr,ranging_sens,tof_sens,direction=0): #0 the rack is on the right  #1 the rack is on the left
    #Assume this sequence is run when the first junction is detected
    for i in range(1,6):
        dist=0
        if direction==0:
            #ToF
            for _ in range(3):
                dist+=tof_sens.get_distance_mm()
                time.sleep(0.1)
            dist/=3
            if dist>ToF_box_constant:
                
        else:
            #Ranging
            for _ in range(3):
                dist+=ranging_sens.read()
                time.sleep(0.1)
            dist/=3
            if dist>Ranging_box_constant:
                
                
                
        
    