from machine import Pin
from utime import sleep

def test_led():
    led_pins = [9, 8, 10, 11]
    leds = []

    for pin in led_pins:
        leds.append(Pin(pin, Pin.OUT))

    while True:
        sleep(0.5)
        for led in leds:
            led.value(1)
        sleep(0.5)
        for led in leds:
            led.value(0)

if __name__ == "__main__":
    test_led()
