EFF_ANGLE_LOOKUP = {0: 0, 90: 1, 180: 2, -90: 3}
ANGLE_AHEAD = 0
ANGLE_RIGHT = 90
ANGLE_LEFT = -90
ANGLE_BEHIND = 180

class Node:
    def __init__(self, id, adj_0deg, adj_90deg, adj_180deg, adj_neg90deg):
        self.id = id
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
    
class Queue:
    def __init__(self):
        self.q = []
        self.rx = 0
 
    def enqueue(self, item):
        self.q.append(item)
 
    def dequeue(self):
        # Queue empty
        if self.rx == len(self.q):
            return None
        self.rx += 1
        return self.q[self.rx - 1]


class Course:
    def __init__(self):
        self.nodes = {0: Node(0, -1, -1, -1, -1)}
        
    '''Update or insert adjacency entry'''
    def _update_or_insert_adj(self, node_id, adjacent_id, adjacency_ind=0):
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id, -1, -1, -1, -1)

        self.nodes[node_id].adj[adjacency_ind] = adjacent_id
        
    '''Add node inserts a node into the graph and handles updating the adjacency list
    of existing adjacent nodes (i.e you don't need to repeat it for each one).

    NOTE: Adjacency angles are measured relative to global direction (see diagram)
    
    Returns the node inserted.
    '''
    def add_node(self, id, adj_0deg, adj_90deg, adj_180deg, adj_neg90deg):
        node = Node(id, adj_0deg, adj_90deg, adj_180deg, adj_neg90deg)

        self.nodes[id] = node

        # Update existing adjacency lists
        # Will be on the opposite side relative to the neighboring node
        if adj_0deg >= 0:
            self._update_or_insert_adj(adj_0deg, id, 2)
        if adj_90deg >= 0:
            self._update_or_insert_adj(adj_90deg, id, 3)
            self.nodes[adj_90deg].adj[3] = id
        if adj_neg90deg >= 0:
            self._update_or_insert_adj(adj_neg90deg, id, 1)
        if adj_180deg >= 0:
            self._update_or_insert_adj(adj_180deg, id, 0)
            
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
        
    '''Calculates the path between start and end (which are target node IDs) which visits the fewest nodes'''
    def shortest_path(self, start, end):
        parents = {start: -1}
        queue = Queue()
        cur = start
 
        while cur is not None and cur != end:
            for node in self.nodes[cur].adj:
                if node == -1:
                    continue
                # If in parents, must have been visited already
                if node not in parents:
                    queue.enqueue(node)
                    parents[node] = cur
                    
            cur = queue.dequeue()
            
        # Backtrack through min-tree to start point, recording nodes passed
        seq = []
        cur = end
        while cur != start:
            seq.append(cur)
            cur = parents[cur]

        return seq[::-1]