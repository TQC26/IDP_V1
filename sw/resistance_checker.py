import time

def resistance(adc0):
    # read ADC input on pin ADC0 as 16-bit integer (0 - 65535)
    adc_value = adc0.read_u16()
    # Convert analog reading (0 - 65535) to a voltage (0 - 3.3V)
    adc_voltage = adc_value * (3.3/65536)
    # send data to computer over USB
    time.sleep(0.5)
    return(adc_voltage)