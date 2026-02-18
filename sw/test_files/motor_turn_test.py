from Subsystems.motor import MOTOR_LEFT, MOTOR_RIGHT, Motor, MotorArray
import time

ADJ_TIME = 0.92

# Init motors
motor_left = Motor(dirPin=7, PWMPin=6)
motor_right = Motor(dirPin=4, PWMPin=5)
mot_arr = MotorArray(motor_left, motor_right)

# Spin and stop
while True:
    mot_arr.spin()
    time.sleep(ADJ_TIME)
    mot_arr.off()

    time.sleep(3)
