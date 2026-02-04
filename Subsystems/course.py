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
    
class Course:
    def __init__(self):
        self.nodes = [Node(0, -1, -1, -1, -1)]
        self.last_node = 0
        
        
    '''Add node inserts a node into the graph and handles updating the adjacency list
    of existing adjacent nodes (i.e you don't need to repeat it for each one).

    NOTE: Adjacency angles are measured relative to global direction (see diagram)
    
    Returns the node inserted.
    '''
    def add_node(self, id, adj_0deg, adj_90deg, adj_180deg, adj_neg90deg):
        node = Node(id, adj_0deg, adj_90deg, adj_180deg, adj_neg90deg)

        self.nodes.append(node)

        # Update existing adjacency lists
        # Will be on the opposite side relative to the neighboring node
        if adj_0deg >= 0 and adj_0deg < len(self.nodes):
            self.nodes[adj_0deg].adj_180deg = id
        if adj_90deg >= 0 and adj_90deg < len(self.nodes): 
            self.nodes[adj_90deg].adj_neg90deg = id
        if adj_neg90deg >= 0 and adj_neg90deg < len(self.nodes):
            self.nodes[adj_neg90deg].adj_90deg = id
        if adj_180deg >= 0 and adj_180deg < len(self.nodes):
            self.nodes[adj_180deg].adj_0deg = id
            
        return node
    
    '''Adds a right hand bend to the track with a finite length (i.e a bay track etc.).
    zdeg direction is use to work out the adjacent node at 0/180 degrees (basically difference from previous/next node).
    stub_id should be -1 unless the stub has an endpoint demarked by an ID'''
    def add_rh_stub(self, id, zdeg_direction=1, stub_id=-1):
        self.add_node(id, id + zdeg_direction, stub_id, id - zdeg_direction, -1)
        
    '''Adds a left hand bend to the track with a finite length (i.e a bay track etc.)
    zdeg direction is use to work out the adjacent node at 0/180 degrees (basically difference from previous/next node).
    stub_id should be -1 unless the stub has an endpoint demarked by an ID'''
    def add_lh_stub(self, id, zdeg_direction=1, stub_id=-1):
        self.add_node(id, id - zdeg_direction, -1, id + zdeg_direction, stub_id)