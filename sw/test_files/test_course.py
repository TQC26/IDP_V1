from sw.course_graph import course, print_course, EFF_ANGLE_LOOKUP

def test_course():
    print_course(course)

    for node_id in course.nodes:
        node = course.nodes[node_id]
        # Check length of adjacency matrix
        for adj in node.adj:
            assert adj < len(course.nodes)
            
        # Check symmetry of adjacency matrix
        # Neighbor at 0 must have us at 180
        # Neighbor at 90 must have us at -90
        # Etc.
        
        # 0 -> 180
        if node.adj[0] != -1:
            assert course.nodes[node.adj[EFF_ANGLE_LOOKUP[0]]].adj[EFF_ANGLE_LOOKUP[180]] == node_id, f"symmetry failed on node {node.id} [0 deg]"
        # 90 -> -90
        if node.adj[1] != -1:
            assert course.nodes[node.adj[EFF_ANGLE_LOOKUP[90]]].adj[EFF_ANGLE_LOOKUP[-90]] == node_id, f"symmetry failed on node {node.id} [90 deg]"
        # 180 -> 0
        if node.adj[2] != -1:
            assert course.nodes[node.adj[EFF_ANGLE_LOOKUP[180]]].adj[EFF_ANGLE_LOOKUP[0]] == node_id, f"symmetry failed on node {node.id} [180 deg]"
        # -90 -> 90
        if node.adj[3] != -1:
            assert course.nodes[node.adj[EFF_ANGLE_LOOKUP[-90]]].adj[EFF_ANGLE_LOOKUP[90]] == node_id, f"symmetry failed on node {node.id} [-90 deg]"
            
if __name__ == "__main__":
    test_course()