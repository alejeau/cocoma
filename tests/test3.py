import numpy as np
import util.miscellaneous as misc

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

print("misc.tc_u_to_u_dist:")

u_dist, u_path = misc.tc_u_to_u_dist((3, -1, 0), (2, -1, 0), graph, edge_lgths,
                                     edges_to_vertices, v_dists, v_paths)

u_dist, u_path = misc.tc_u_to_u_dist((3, 0, 0), (2, 0, 0), graph, edge_lgths,
                                     edges_to_vertices, v_dists, v_paths)

print(u_dist, u_path)
print("\n")


