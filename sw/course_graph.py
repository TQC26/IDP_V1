from Subsystems.course import *

'''Print the course adjacency lists for debugging'''
def print_course(course):
    for node_id in course.nodes:
        node = course.nodes[node_id]
        print("[Node %d]: 0: %d, 90: %d, 180: %d, -90: %d" % (node.id, node.adj[0], node.adj[1], node.adj[2], node.adj[3]))

# Defines global course adjacency list
course = Course()

# Node zero already inserted (the tee at the exit) to the start box
# The rest of the nodes should proceed CW around the track
# Lack of connection represented by -1
course.add_node(1, -1, 0, 36, 2)
course.add_node(2, 3, 1, 37, -1)

# Rack A lower bays
bay_a6l = course.add_rh_stub(3)
bay_a5l = course.add_rh_stub(4)
bay_a4l = course.add_rh_stub(5)
bay_a3l = course.add_rh_stub(6)
bay_a2l = course.add_rh_stub(7)
bay_a1l = course.add_rh_stub(8)

course.add_node(9, -1, 10, 8, -1)
course.add_node(10, -1, 11, 20, 9)
course.add_node(11, -1, -1, 12, 10)

# Rack B lower bays
bay_a6l = course.add_lh_stub(12)
bay_a5l = course.add_lh_stub(13)
bay_a4l = course.add_lh_stub(14)
bay_a3l = course.add_lh_stub(15)
bay_a2l = course.add_lh_stub(16)
bay_a1l = course.add_lh_stub(17)

course.add_node(18, 17, -1, 39, 19)
course.add_node(19, -1, 18, 38, 0)

# Loading bays
pickup_4 = course.add_node(39, 18, -1, -1, -1)
pickup_3 = course.add_node(38, 19, -1, -1, -1)
pickup_2 = course.add_node(36, 1, -1, -1, -1)
pickup_1 = course.add_node(37, 2, -1, -1, -1)

# Start point
start_point = course.add_node(35, 0, -1, -1, -1)

# Upstairs nodes
course.add_node(20, 10, 22, -1, 21)
course.add_node(21, 23, 20, -1, -1)
course.add_node(22, 24, -1, -1, 20)

# Rack A upper bays
bay_a1u = course.add_lh_stub(23, -2)
bay_a2u = course.add_lh_stub(25, -2)
bay_a3u = course.add_lh_stub(27, -2)
bay_a4u = course.add_lh_stub(29, -2)
bay_a5u = course.add_lh_stub(31, -2)
bay_a6u = course.add_node(33, -1, -1, 31, -1)   # Special case due to track end

# Rack B upper bays
bay_b1u = course.add_rh_stub(24, 2)
bay_b2u = course.add_rh_stub(26, 2)
bay_b3u = course.add_rh_stub(28, 2)
bay_b4u = course.add_rh_stub(30, 2)
bay_b5u = course.add_rh_stub(32, 2)
bay_b6u = course.add_node(34, -1, -1, 32, -1)   # Special case due to track end