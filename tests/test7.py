# Test of misc.to_tc_path through misc.tc_u_to_u_dist and of
# misc.tc_u_to_u_dists

import numpy as np
import util.miscellaneous as misc

from model.space.Space import Space

branch_number = 6
vertices_number = branch_number + 1
edges_number = 2 * branch_number

# I.1.1. space initialization

graph = np.array([[-1, 0, 1, 2, 3, 4, 5],
                  [0, -1, 6, -1, -1, -1, 11],
                  [1, 6, -1, 7, -1, -1, -1],
                  [2, -1, 7, -1, 8, -1, -1],
                  [3, -1, -1, 8, -1, 9, -1],
                  [4, -1, -1, -1, 9, -1, 10],
                  [5, 11, -1, -1, -1, 10, -1]], dtype=np.int16)

# I.1.2. Edge features initialization
edge_lgths = []
for _ in range(branch_number):
    edge_lgths.append(4)

for _ in range(6, edges_number):
    edge_lgths.append(6)

edge_lgths = np.array(edge_lgths, dtype=np.int16)

edges_to_vertices = np.empty([len(edge_lgths), 2], dtype=np.int16)
for i in range(len(graph)):
    # Retrieval of the existing edges' indices ( > -1) in the column
    #  of the edges of i
    for j in np.argwhere(graph[i] > -1):
        edges_to_vertices[graph[i][j]] = [i, j]

max_units_of_edge = edge_lgths.max()

locations = np.array([], np.float32)

edge_activations = np.ones(edge_lgths, dtype=np.int16)

ngbrs = misc.build_tc_neighbours(graph)

v_dists, v_paths = misc.fw_distances(graph, edge_lgths)

'''
dists, paths = misc.tc_u_to_u_dists(graph, edge_lgths,
                                    edges_to_vertices,
                                    max_units_of_edge, v_dists,
                                    v_paths)

space = Space(graph, edges_to_vertices, edge_lgths,
              max_units_of_edge, edge_activations, locations,
              ngbrs, dists, paths, v_dists)
'''

# I.1.3. Idlenesses
idls = [0] * len(graph)

print("misc.to_tc_path\n")
v_1_1 = (6, -1, 0)
v_1_2 = (0, -1, 0)
v_e_1 = (5, -1, 0)
v_e_2 = (2, -1, 0)
p_1 = (3, 8, 4)
p_2 = (4, 9, 3)
ls = [v_1_1, v_1_2, v_e_1, v_e_2, p_1, p_2]

for l1 in ls:
    for l2 in ls:
        print(l1, l2)
        vp = v_paths[l1[0]][l2[0]]
        print(vp)
        # u_dist = misc.to_tc_path(l1, l2, v_paths[l1[0]][l2[0]], graph,
        #                          edge_lgths, edges_to_vertices, v_dists)
        u_dist = misc.tc_u_to_u_dist(l1, l2, graph, edge_lgths,
                                     edges_to_vertices, v_dists)
        print(u_dist, "\n")

'''
print(paths[4][9][3][3][8][4])
print(paths[4][9][3][3][8][0])
print(paths[0][0][0][2][1][0])
'''

l1, l2 = (4, 9, 5), (4, 9, 5)
print(l1, l2, " The same positions:")
u_dist = misc.tc_u_to_u_dist(l1, l2, graph, edge_lgths,
                             edges_to_vertices, v_dists)
print(u_dist, "\n")

l1, l2 = (4, 9, 3), (3, 8, 4)
print(l1, l2)
u_dist = misc.tc_u_to_u_dist(l1, l2, graph, edge_lgths,
                             edges_to_vertices, v_dists)
print(u_dist, "\n")

l1, l2 = (4, 9, 3), (3, 8, 0)
print(l1, l2)
u_dist = misc.tc_u_to_u_dist(l1, l2, graph, edge_lgths,
                             edges_to_vertices, v_dists)
print(u_dist, "\n")

l1, l2 = (0, 0, 0), (2, 1, 0)
print(l1, l2)
u_dist = misc.tc_u_to_u_dist(l1, l2, graph, edge_lgths,
                             edges_to_vertices, v_dists)
print(u_dist, "\n")

l1, l2 = (4, 9, 3), (4, 9, 5)
print(l1, l2, " Positions located on the same edge. The edge must be climbed "
              "up:")
u_dist = misc.tc_u_to_u_dist(l1, l2, graph, edge_lgths,
                             edges_to_vertices, v_dists)
print(u_dist, "\n")

l1, l2 = (4, 9, 5), (4, 9, 3)
print(l1, l2, " Positions located on the same edge. The edge must be came "
              "down:")
u_dist = misc.tc_u_to_u_dist(l1, l2, graph, edge_lgths,
                             edges_to_vertices, v_dists)
print(u_dist, "\n")

l1, l2 = (1, 11, 5), (6, 11, 5)
print(l1, l2, " Positions in the opposite direction from the same edge. The "
              "edge must be climbed up:")
u_dist = misc.tc_u_to_u_dist(l1, l2, graph, edge_lgths,
                             edges_to_vertices, v_dists)
print(u_dist, "\n")

l1, l2 = (1, 11, 3), (6, 11, 1)
print(l1, l2, " Positions in the opposite direction from the same edge. The "
              "edge must be came down:")
u_dist = misc.tc_u_to_u_dist(l1, l2, graph, edge_lgths,
                             edges_to_vertices, v_dists)
print(u_dist, "\n")

u_dists = misc.tc_u_to_u_dists(graph, edge_lgths, edges_to_vertices, v_dists)
print(u_dists[1][11][3][3][8][5])