import time

def resistance(adc0):
    # read ADC input on pin ADC0 as 16-bit integer (0 - 65535)
    adc_value = adc0.read_u16()
    # Convert analog reading (0 - 65535) to a voltage (0 - 3.3V)
    adc_voltage = adc_value * (3.3/65536)
    # send data to computer over USB
    time.sleep(0.5)
    return(adc_voltage)

def reel_type_to_node(adc0):
    # read ADC input on pin ADC0 as 16-bit integer (0 - 65535)
    adc_sum=0
    for i in range (5):
        adc_value = adc0.read_u16()
        adc_voltage = adc_value * (3.3/65536)
        adc_sum+=adc_voltage
        time.sleep(0.1)
    adc_sum/=5
    #Left_bottom (0),Left_upper (1),Right_upper (2),Right_bottom (3)

    if adc_sum>2.6: #Yellow, right_bottom
        return 17
    elif adc_sum>2.3: #Red, right_upper
        return 24
    elif adc_sum>1: #Green, left_upper
        return 23
    else: # Blue, left_bottom
        return 3
        
    
        