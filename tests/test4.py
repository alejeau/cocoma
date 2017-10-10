# Test for the method misc.compute_dists_to_agts

import numpy as np
import util.miscellaneous as misc
import copy

from control.agent.Agent import Agent
from model.knowledge.EnvironmentKnowledge import EnvironmentKnowledge
from model.space.Space import Space
from util.net.SimulatedConnection import SimulatedConnection

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

dists, paths = misc.tc_u_to_u_dists(graph, edge_lgths,
                                    edges_to_vertices,
                                    max_units_of_edge, v_dists,
                                    v_paths)

space = Space(graph, edges_to_vertices, edge_lgths,
                   max_units_of_edge, edge_activations, locations,
                   ngbrs, dists, paths, v_dists, v_paths)

# I.1.3. Idlenesses
idls = [0] * len(graph)

# I.2. Agents

# I.2.1. Agent Position
# Initial agents positions
for i in range(len(graph)):
    for j in graph[i][graph[i] > -1]:
        for k in range(edge_lgths[j]):
            for l in range(len(graph)):
                for m in graph[l][graph[l] > -1]:
                    for n in range(edge_lgths[m]):
                        agts_pos = np.array([[i, j, k], [l, m, n]],
                                            dtype=np.int16)

                        print("misc.compute_dists_to_agts\n", agts_pos[0], " ",
                              agts_pos[1], "\n agent 0:")
                        print(misc.compute_dists_to_agts(0, agts_pos, graph,
                                                         edge_lgths,
                                                         edges_to_vertices,
                                                         v_dists))
                        print("agent 1:")
                        print(misc.compute_dists_to_agts(1, agts_pos, graph,
                                                         edge_lgths,
                                                         edges_to_vertices,
                                                         v_dists))

for i in range(len(graph)):
    for l in range(len(graph)):
        for m in graph[l][graph[l] > -1]:
            for n in range(edge_lgths[m]):
                agts_pos = np.array([[i, -1, 0], [l, m, n]],
                                    dtype=np.int16)
                print("misc.compute_dists_to_agts\n", agts_pos[0], " ",
                      agts_pos[1], "\n agent 0:")
                print(misc.compute_dists_to_agts(0, agts_pos, graph,
                                                 edge_lgths,
                                                 edges_to_vertices,
                                                 v_dists))
                print("agent 1:")
                print(misc.compute_dists_to_agts(1, agts_pos, graph,
                                                 edge_lgths,
                                                 edges_to_vertices,
                                                 v_dists))

for i in range(len(graph)):
    for j in graph[i][graph[i] > -1]:
        for k in range(edge_lgths[j]):
            for l in range(len(graph)):
                agts_pos = np.array([[i, j, k], [l, -1, 0]],
                                    dtype=np.int16)

                print("misc.compute_dists_to_agts\n", agts_pos[0], " ",
                      agts_pos[1], "\n agent 0:")
                print(misc.compute_dists_to_agts(0, agts_pos,
                                                 edge_lgths,
                                                 edges_to_vertices,
                                                 v_dists))
                print("agent 1:")
                print(misc.compute_dists_to_agts(1, agts_pos,
                                                 edge_lgths,
                                                 edges_to_vertices,
                                                 v_dists))

for i in range(len(graph)):
    for l in range(len(graph)):
        agts_pos = np.array([[i, -1, 0], [l, -1, 0]],
                            dtype=np.int16)
        print("misc.compute_dists_to_agts\n", agts_pos[0], " ",
              agts_pos[1], "\n agent 0:")
        print(misc.compute_dists_to_agts(0, agts_pos, graph,
                                         edge_lgths,
                                         edges_to_vertices,
                                         v_dists))
        print("agent 1:")
        print(misc.compute_dists_to_agts(1, agts_pos, graph,
                                         edge_lgths,
                                         edges_to_vertices,
                                         v_dists))