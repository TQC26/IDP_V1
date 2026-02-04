EFF_ANGLE_LOOKUP = {0: 0, 90: 1, 180: 2, -90: 3}
ANGLE_AHEAD = 0
ANGLE_RIGHT = 90
ANGLE_LEFT = -90
ANGLE_BEHIND = 180

class Node:
    def __init__(self, id, adj_0deg, adj_90deg, adj_180deg, adj_neg90deg):
        self.node_id = id
        self.adj = [adj_0deg, adj_90deg, adj_180deg, adj_neg90deg]
        
    '''Returns the node which is adjacent to the current one at the angle
    measured relative to the heading (i.e 0 deg is straight ahead and 90 is right).

    Heading and angle must be in [-90 180].
    '''
    def get_adjacent(self, angle, heading):
        assert -90 <= heading <= 180
        assert -90 <= angle <= 180
        
        eff_angle = angle - heading
        if eff_angle > 180:
            eff_angle = 360 - eff_angle

        return self.adj[EFF_ANGLE_LOOKUP[eff_angle]]