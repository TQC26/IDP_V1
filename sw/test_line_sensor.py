from machine import Pin
from utime import sleep

from libs.line_follower.DFRobot_SEN0017 import DFRobot_SEN0017

def test_line_sensor():
    led_pin = 28  # Pin 28 = GP28 (labelled 34 on the jumper)
    led = Pin(led_pin, Pin.OUT)
    
    sens_pin = 22 # GPT22
    sens = DFRobot_SEN0017(sens_pin)

    while True:
        print("Polling sensor")
        if sens.on_line():
            print("On line")
            led.value(1)
        else:
            led.value(0)
        sleep(0.5)

if __name__ == "__main__":
    test_line_sensor()