from machine import Pin

'''Simple interface class for the line following sensor.
   Reserves the pin which the sensor is on for itself (set to read).
'''
class DFRobot_SEN0017:
    def __init__(self, sensPin):
        self.pin = Pin(sensPin, Pin.IN)

    '''Returns true for the sensor reading white (above a line)'''
    def on_line(self):
        cnt=0
        for i in range(0,4):
            if self.pin.value() == 1:
                cnt+=1
        
        if cnt>=3:
            return 1
        else:
            return 0
        