# Test of misc.to_tc_path through misc.tc_u_to_u_dist and of
# misc.tc_u_to_u_dists

import numpy as np
import util.miscellaneous as misc
from model.Paths import Paths

from model.space.Space import Space

path = Paths.Sim_materials + "cr-islands-soc_0_10-0.xml"

graph, fl_edge_lgths = misc.sim_xml_to_iterables(path)
edge_lgths = np.int16(np.round(fl_edge_lgths))

edges_to_vertices = np.empty([len(edge_lgths), 2], dtype=np.int16)
for i in range(len(graph)):
    # Retrieval of the existing edges' indices ( > -1) in the column
    #  of the edges of i
    for j in np.where(graph[i] > -1)[0]:
        edges_to_vertices[graph[i][j]] = [i, j]

max_units_of_edge = edge_lgths.max()

locations = np.array([], np.float32)

edge_activations = np.ones(len(edge_lgths), dtype=np.int16)

ngbrs = misc.build_tc_neighbours(graph)

v_dists, v_paths = misc.fw_distances(graph, edge_lgths)

dists = misc.tc_u_to_u_dists(graph, edge_lgths, edges_to_vertices,
                             v_dists)
# I.1.3. Idlenesses
idls = [0] * len(graph)

p1 = (5, -1, 0)
p2 = (3, -1, 0)

path = misc.to_tc_path(p1, p2, v_paths[p1[0]][p2[0]], graph, edge_lgths,
                       edges_to_vertices)
print(v_paths[p1[0]][p2[0]])
print(v_dists[p2[0]][p1[0]])
print(path)

print(dists[3][23][5][28][38][1])
print(dists[28][38][1][3][23][5])

