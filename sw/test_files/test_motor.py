from machine import Pin, PWM
from utime import sleep
from Subsystems.motor import Motor


def test_motor3():
    motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP4/5

    while True:
        print("Forward")
        motor3.Forward()
        sleep(1)
        print("Reverse")
        motor3.Reverse()
        sleep(1)


if __name__ == "__main__":
    test_motor3()
