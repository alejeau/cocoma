import numpy as np
import util.miscellaneous as misc
from model.space.Space import Space

# I. Configuration

# I.1. Environment

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

ngbrs = misc.build_neighbours(graph)

v_dists, v_paths = misc.fw_distances(graph, edge_lgths)

u_dists, u_paths = misc.tc_u_to_u_dists(graph, edge_lgths,
                                       edges_to_vertices,
                                       max_units_of_edge, v_dists,
                                       v_paths)

space = Space(graph, edges_to_vertices, edge_lgths,
              max_units_of_edge, edge_activations, locations,
              ngbrs, u_dists, u_paths,)

tc_v_dist, tc_v_path = misc.tc_v_to_v_dist((0, -1, 0), (4, 8, 6),
                                           graph, edge_lgths,
                                           space.edges_to_vertices, v_dists,
                                           v_paths)

print(tc_v_dist, tc_v_path)

three_c_v_dists = misc.tc_v_to_v_dists((0, 0, 0), graph, edge_lgths,
                                       space.edges_to_vertices,
                                       space.max_units_of_edge,
                                       v_dists, v_paths)
print(three_c_v_dists[1])

tc_dist, tc_path = misc.tc_u_to_u_dist((0, -1, 0), (1, 6, 2), graph,
                                       edge_lgths,
                                       space.edges_to_vertices, v_dists,
                                       v_paths)
print(tc_dist, tc_path)

dists, paths = misc.tc_u_to_u_dists(graph, edge_lgths, space.edges_to_vertices,
                                    space.max_units_of_edge, v_dists, v_paths)

print("misc.tc_u_to_u_dists:")
print(dists[0, 0, 0, 1, 6, 2])
print(paths[0][0][0][1][6][2])
print("\n")

print("Space.dist: ", space.dist((0, -1, 0), (1, 6, 2)))
print("Space.path: ", space.path((0, -1, 0), (1, 6, 2)))
