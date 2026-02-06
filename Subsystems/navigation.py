import line_to_junction as ltj

TURN_MODE_LOOKUP = {
        0: 2,   # Drive straight
        90: 1,  # Turn right
        -90: 0, # Turn left
}

'''Stores current location and heading'''
class Location:
    def __init__(self, initialNode, motorArray, sensorArray, course, initialHeading=0):
        self.node = initialNode
        self.heading = initialHeading
        self.motArr = motorArray
        self.sensArr = sensorArray
        self.course = course

    '''Returns ang adjusted to be relative to the current heading.
    Returned angles are always in [-90 180], as should the angles passed.'''
    def relative_angle(self, ang):
        assert -90 <= ang <= 180
        rel = ang - self.heading
        if rel > 180:
            rel = 360 - ang

    '''Drive to a node, possibly passing by other nodes in the process''' 
    def drive_to_node(self, target, speed=40):
        # Calculate shortest path to destination
        path = course.shortest_path(self.node, target)

        for tgt_node in path:
            direct = self.relative_angle(self.course[self.node].find_adjacent_ang(tgt_node))
            junction_turn(self.motArr, self.sensArr, TURN_MODE_LOOKUP[direct])

            self.heading = self.course[self.node].find_adjacent_ang(tgt_node)
            drive_until_junction(self.motArr, self.sensArr, speed=speed)
            self.node = tgt_node