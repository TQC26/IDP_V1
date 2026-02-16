import time

def resistance(adc0):
    # read ADC input on pin ADC0 as 16-bit integer (0 - 65535)
    adc_value = adc0.read_u16()
    # Convert analog reading (0 - 65535) to a voltage (0 - 3.3V)
    adc_voltage = adc_value * (3.3/65536)
    # send data to computer over USB
    time.sleep(0.5)
    return(adc_voltage)

def reel_type_to_node(adc0,led_arr):
    adc_sum=0
    for i in range (10):
        adc_value = adc0.read_u16()
        adc_voltage = adc_value * (3.3/65536)
        adc_sum+=adc_voltage
        time.sleep(0.1)
    adc_sum/=10
    #Left_bottom (0),Left_upper (1),Right_upper (2),Right_bottom (3)

    if adc_sum>2.35: #Yellow, right_bottom 17=3
        led_arr[0].value(1)
        return 17
    elif adc_sum>1.6: #Red, right_upper 24=2
        led_arr[1].value(1)
        return 24
    elif adc_sum>0.65: #Green, left_upper 23=1
        led_arr[2].value(1)
        return 23
    else: # Blue, left_bottom 3=0
        led_arr[3].value(1)
        return 3
def lightsoff(led_arr):
    for i in range(4):
        led_arr[i].value(0)