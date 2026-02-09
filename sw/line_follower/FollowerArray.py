from line_follower.DFRobot_SEN0017 import DFRobot_SEN0017

JUNCTION_TYPE_NONE = 0      # No junction detected
JUNCTION_TYPE_RIGHT = 1     # A right hand bend in the track
JUNCTION_TYPE_LEFT = 2      # A left hand bend in the track
JUNCTION_TYPE_TEE = 3       # A junction with more than one possible path joined at a T shape

'''FollowerArray represents a set of line followers from which results can
be queried. The array should be four sensors in width.
'''
class FollowerArray:
    '''Pins is an array of length four containing the GPIO pin numbers for the sensors in
    the array. Pins should begin from left to right.'''
    def __init__(self, pins):
        self.array = []
        for pin in pins:
            self.array.append(DFRobot_SEN0017(pin))
    '''Uses the follower array to detect if a junction is under the front of the chasis.
    IMPORTANT NOTE: A "tee" junction will be counted as a left/right hand bend if going
                    straight on is a valid path (for instance, the turn on to the ramp
                    is a right hand turn (from heading 90deg) not a tee).
    '''
    def detect_junction(self):
        left_hand = self.array[0].on_line() and self.array[1].on_line()
        right_hand = self.array[2].on_line() and self.array[3].on_line()

        if left_hand and right_hand:
            return JUNCTION_TYPE_TEE
        elif left_hand:
            return JUNCTION_TYPE_LEFT
        elif right_hand:
            return JUNCTION_TYPE_RIGHT
        else:
            return JUNCTION_TYPE_NONE