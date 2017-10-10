# Test of misc.to_tc_path through misc.tc_u_to_u_dist and of
# misc.tc_u_to_u_dists

import numpy as np
import util.miscellaneous as misc

from model.space.Space import Space

graph = np.ones([9, 9], dtype=np.int16) * -1
graph[0][1] = 0
graph[1][0] = 0

graph[1][2] = 1
graph[2][1] = 1

graph[1][3] = 2
graph[3][1] = 2

graph[2][3] = 3
graph[3][2] = 3

graph[3][4] = 4
graph[4][3] = 4

graph[4][5] = 5
graph[5][4] = 5

graph[5][6] = 6
graph[6][5] = 6

graph[6][3] = 7
graph[3][6] = 7

graph[4][7] = 8
graph[7][4] = 8

graph[4][8] = 9
graph[8][4] = 9

edge_lgths = np.ones([10], dtype=np.int16)
edge_lgths[0] = 5
edge_lgths[1] = 1
edge_lgths[2] = 6
edge_lgths[3] = 8
edge_lgths[4] = 2
edge_lgths[5] = 1
edge_lgths[6] = 3
edge_lgths[7] = 4
edge_lgths[8] = 7
edge_lgths[9] = 9

edges_to_vertices = np.empty([len(edge_lgths), 2], dtype=np.int16)
for i in range(len(graph)):
    # Retrieval of the existing edges' indices ( > -1) in the column
    #  of the edges of i
    for j in np.where(graph[i] > -1)[0]:
        # np.where returns a tuple

        edges_to_vertices[graph[i][j]] = [i, j]

max_units_of_edge = edge_lgths.max()

locations = np.array([], np.float32)

edge_activations = np.ones(len(edge_lgths), dtype=np.int16)

ngbrs = misc.build_tc_neighbours(graph)

v_dists, v_paths = misc.fw_distances(graph, edge_lgths)

# I.1.3. Idlenesses
idls = [0] * len(graph)

p1 = (5, -1, 0)
p2 = (3, -1, 0)

path = misc.to_tc_path(p1, p2, v_paths[p1[0]][p2[0]], graph, edge_lgths,
                       edges_to_vertices)
print(v_paths[p1[0]][p2[0]])
print(v_dists[p2[0]][p1[0]])
print(v_dists)

# for i in range(len(graph)):
#    print(graph[i], '\n')
