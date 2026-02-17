from Subsystems.motor import MOTOR_LEFT, MOTOR_RIGHT, Motor, MotorArray
from Subsystems.servo import Servo
from machine import Pin, SoftI2C, I2C
from line_follower.DFRobot_SEN0017 import DFRobot_SEN0017
from line_follower.FollowerArray import FollowerArray
import line_to_junction
import resistance_checker
import time

# Limits for range finder
Dist_min=100
Dist_max=250

# Limits for time of flight
# TODO: Tune!
Dist_TOF_min=140
Dist_TOF_max=200

RACK_JUNCTION_ADJUST_TIME = 0.6

#0 is unknown, 1 is box
rack_info=[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]] #Left_bottom (0),Left_upper (1),Right_upper (2),Right_bottom (3)

def junction_sequence(mot_arr,sens_arr,servo_arr,ranging_sens,tof_sens,led_arr,rack=0):
    #Assume this sequence is run when the first junction is detected
    i=1
    while i<=6:
        mot_arr.tank(40, 40)
        time.sleep(0.2)

        dist=0
        if rack%2==0:
            #ToF
            for _ in range(10):
                dist+=tof_sens.get_distance_mm()
                time.sleep(0.1)
            dist/=10
            print(f"avg bay distance: {dist}mm")
            if rack_info[rack][i - 1]==1:
                line_to_junction.junction_turn(mot_arr,sens_arr,2,bay=False)
                line_to_junction.drive_until_junction(mot_arr, sens_arr,95,0)
            elif dist<Dist_TOF_max and dist>Dist_TOF_min:
                rack_info[rack][i - 1]=1
                line_to_junction.junction_turn(mot_arr,sens_arr,2,bay=False)
                line_to_junction.drive_until_junction(mot_arr, sens_arr,95,0)
            else:
                rack_info[rack][i - 1]=1
                mot_arr.tank(50, 50)
                time.sleep(RACK_JUNCTION_ADJUST_TIME)
                line_to_junction.junction_turn(mot_arr,sens_arr,1, bay=True)
                line_to_junction.junction_alignment(mot_arr,sens_arr)
                time.sleep(2)
                line_to_junction.offload(mot_arr,servo_arr)
                break            
        else:
            #Ranging
            for _ in range(10):
                dist+=ranging_sens.read()
                time.sleep(0.1)
            dist/=10
            print(f"avg bay distance: {dist}mm")
            if rack_info[rack][i - 1]==1:
                print("bay occupied")
                line_to_junction.junction_turn(mot_arr,sens_arr,2,bay=False)
                line_to_junction.drive_until_junction(mot_arr, sens_arr,95,0)
            elif dist<Dist_max and dist>Dist_min:
                print("bay occupied [new]")
                rack_info[rack][i - 1]=1
                line_to_junction.junction_turn(mot_arr,sens_arr,2,bay=False)
                line_to_junction.drive_until_junction(mot_arr, sens_arr,95,0)
            else:
                print("selecting bay")
                rack_info[rack][i - 1]=1
                mot_arr.tank(50, 50)
                time.sleep(RACK_JUNCTION_ADJUST_TIME)
                line_to_junction.junction_turn(mot_arr,sens_arr,0, bay=True)
                line_to_junction.junction_alignment(mot_arr,sens_arr)
                time.sleep(2)
                line_to_junction.offload(mot_arr,servo_arr)
                break
        i+=1
    resistance_checker.lightsoff(led_arr)
    line_to_junction.junction_leave(mot_arr,sens_arr,rack)

    if i > 2:
        line_to_junction.drive_until_junction(mot_arr, sens_arr,75,i-3)
