# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

import json

import numpy as np
import untangle


def retrieve_neighbours(v: int, graph: np.ndarray) -> np.ndarray:
    t = np.nonzero(graph[v] + 1)
    # + 1 because the indexing of vertices starts from 0. So adding 1
    # enables to get only the indices whose the values are not equal to -1

    return t[0]


def build_neighbours(g: np.ndarray) -> list:
    l = []
    for i in range(len(g)):
        i_neighbours = retrieve_neighbours(i, g)
        l.append(i_neighbours.tolist())
    return l


def build_tc_neighbours(g: np.ndarray) -> list:
    """
    :param g: the current graph
    :type g: np.ndarray
    :return:
    :rtype: list
    """
    tc_ngbrs = []
    ngbrs = build_neighbours(g)

    for ns in ngbrs:
        tc_n = []
        for v in ns:
            tc_n += [(v, -1, 0)]
        tc_ngbrs += [tc_n]

    return tc_ngbrs


# Floyd-Warshall Algorithm
def fw_distances(graph, edge_lgths) -> (np.ndarray, list):
    """
    :param graph:
    :type graph: 2-D iterable
    :param edge_lgths:
    :type edge_lgths: 1-D iterable
    :return: a 2-uplet consisting of a numpy ndarray of all distances
    between vertices and a list of all paths.
    :rtype: (np.ndarray, list)
    """

    infini = edge_lgths.max() + 10000

    # let dists be a |V| × |V| array of minimum distances initialized to
    # infinity
    dists = np.zeros(graph.shape, dtype=np.int16) + infini
    paths = [[[i] for _ in range(len(graph))] for i in range(len(graph))]

    # for each vertex i
    for i in range(len(graph)):
        for j in range(len(graph)):
            if graph[i][j] != -1:
                dists[i][j] = edge_lgths[graph[i][j]]
                paths[i][j] += [j]

        paths[i][i] += [i]
        dists[i][i] = 0

    for k in range(len(graph)):
        for i in range(len(graph)):
            for j in range(len(graph)):
                if dists[i][j] > dists[i][k] + dists[k][j]:
                    dists[i][j] = dists[i][k] + dists[k][j]
                    paths[i][j] = paths[i][k] + paths[k][j][1:]

    # np.place(dists, dists==infini, -1)

    return dists, paths


def to_tc_path(pos1, pos2, v_path, graph, edge_lgths, edges_to_vertices) -> \
        list:
    """
    :param edges_to_vertices:
    :param pos1:
    :type pos1: 3-D tuple
    :param pos2:
    :type pos2: 3-D tuple
    :param graph:
    :type graph: 2-D iterable
    :param edge_lgths:
    :type edge_lgths: 2-D iterable
    :param v_path: list of the vertices' paths to convert into a list of
    3-coordinate positions
    :type v_path: list
    :return: returns the 3-coordinated  path of the successive 3-coordinate
    positions from the provided vertices' path v_path between pos1 and pos2. It
    works only with the positions representing vertices and not with
    positions representing units of edge
    :rtype: list
    """

    path = [pos1]

    # Current pos
    pos = pos1

    if pos1[0] != pos2[0]:
        for i in range(len(v_path) - 1):
            # Current edge
            ce = graph[pos[0]][v_path[i + 1]]

            pos = (pos[0], ce, pos[2])

            for u in range(pos[2] + 1, edge_lgths[ce]):
                path += [(pos[0], ce, u)]

            pos = (v_path[i + 1], -1, 0)

            path += [pos]
    else:
        if pos1[1] == pos2[1]:
            path += [pos2]
        else:
            path += [pos2]
            # TODO: fixing the issue corresponding to the above case where
            # pos1[0] == pos2[0]

    return path


def target(s: int, e: int, graph, edges_to_vertices) -> int:
    """
    :param graph:
    :type graph:
    :param s: the source whence the edge is stemmed from
    :type s: int
    :param e: the edge whose the target is requested
    :type e: int
    :param edges_to_vertices:
    :type edges_to_vertices: 2-D iterable
    :return: the heading vertex when coming from s on the edge e
    :rtype: int
    """

    # e = graph[s][graph[s] > -1][0] if e == -1 else e

    if e == -1:
        raise ValueError("Value -1 forbidden. Edge's id must be higher than "
                         "-1")

    return edges_to_vertices[e][edges_to_vertices[e] != s][0]


def edge(v0: int, v1: int, graph) -> int:
    return graph[v0][v1]


def compute_dists_to_agts(agt_id: int, agts_pos: np.ndarray, space) \
        -> np.ndarray:
    agts_dists = np.ones(len(agts_pos), dtype=np.int16) * -1

    for i in range(len(agts_dists)):
        agts_dists[i] = space.dist((agts_pos[agt_id][0], agts_pos[agt_id][1],
                                    agts_pos[agt_id][2]), (agts_pos[i][0],
                                                           agts_pos[i][1],
                                                           agts_pos[
                                                               i][2]))

    return agts_dists


def former_compute_dists_to_agts(agt_id: int, agts_pos: np.ndarray, graph,
                                 edge_lgths, edges_to_vertices,
                                 v_dists) -> np.ndarray:
    """
    :param agt_id: The id of agent from which the distances of each others
    are computed
    :type agt_id: int
    :param space:
    :type space: Space
    :param agts_pos: a int16 numpy.ndarray of shape (<agent number>, 3)
    :type agts_pos: numpy.ndarray
    :return: dists_to_agts: The distance of agt_id to others agents
    :rtype: dists_to_agts: numpy.ndarray
    """

    if agts_pos[agt_id][1] == -1 and agts_pos[agt_id][2] != 0:
        raise ValueError(
            "A vector of the the 3D space of positions with an edge "
            "coordinate (2nd coordinate) valued to -1 cannot have a unit "
            "coordinate (3rd coordinate) higher than 0.")

    # Distances of agt_id to the whole vertices
    agt_id_to_vertices = v_dists[agts_pos[agt_id][0]]

    # If the agent agt_id is travelling an edge
    if agts_pos[agt_id][1] > -1 and agts_pos[agt_id][2] > 0:
        # Distance to the others agents computed by crossing the source
        # of its edge
        dists_from_source = v_dists[agts_pos[agt_id][0]] + \
                            agts_pos[agt_id][2]

        # Distance to the others agents computed by crossing the target
        # of its edge
        dists_from_target = v_dists[target(agts_pos[agt_id][0],
                                           agts_pos[agt_id][1], graph,
                                           edges_to_vertices)] + edge_lgths[
                                agts_pos[agt_id][1]] - agts_pos[agt_id][2]

        # Distance to the others agents dists_to_agts is finally the min of
        #  both
        agt_id_to_vertices = \
            dists_from_source * (dists_from_source < dists_from_target) \
            + dists_from_target * (1 - (dists_from_source <
                                        dists_from_target))
        # Another way to carry out the previous operation:
        # agt_id_to_vertices =\
        # np.where( (dists_from_source < dists_from_target),
        #           dists_from_source,
        #           dists_from_target )

    # Taking the 1st value (index 0) of the second axis (axis 1) of
    # agts_pos, to get the distance of each agent from the current agent
    #  `agt_id`
    dists_to_agts = agt_id_to_vertices[agts_pos.take(0, axis=1)]
    # Another way to carry out the previous operation:
    # dists_to_agts = agt_id_to_vertices[agts_pos[:, 0]]

    # At that stage dists_to_agts represents the distance from
    # agt_id to others agents regardless of its position (travelling
    # an edge or on a vertex)

    agts_on_edge = np.where(agts_pos[:, 1] > -1)[0]
    # Others ways to carry out the previous operation:
    # agts_on_edge = np.where(agts_pos.take(1, axis=1) > -1)[0]

    for a in agts_on_edge:
        if agts_pos[a][1] == agts_pos[agt_id][1]:
            dists_to_agts[a] = np.absolute(agts_pos[a][2] - agts_pos[
                agt_id][2])
        else:
            dists_to_agts[a] = \
                np.minimum(agt_id_to_vertices[agts_pos[a][0]] + agts_pos[a][2],
                           agt_id_to_vertices[target(agts_pos[a][0],
                                                     agts_pos[a][1],
                                                     graph,
                                                     edges_to_vertices)] +
                                   edge_lgths[agts_pos[a][1]] - agts_pos[a][2])

    return dists_to_agts


def tc_v_to_v_dist(pos1, pos2, graph: np.ndarray, edge_lgths,
                   edges_to_vertices, v_dists: np.ndarray) -> int:
    """
    :param pos1:
    :type pos1: 3-D tuple
    :param pos2:
    :type pos2: 3-D tuple
    :param graph:
    :type graph: 2-D iterable
    :param edge_lgths:
    :type edge_lgths: 1-D iterable
    :param edges_to_vertices:
    :type edges_to_vertices: 2-D iterable
    :param v_dists:
    :type v_dists: np.ndarray
    :param v_paths: a 3-dimensional list of all vertex-to-vertex paths
    where every path contains the vertices between the pos1's vertex (
    excluded) and the pos2's one
    :type v_paths:
    :return: a np.ndarray of the vertex-to-vertex distances between two
    positions in 3-coordinate ( (v, e, u) ) and an array of the path of
    successive vertex in 1-coordinate. Regardless the positions passed in
    parameters, only the vertex, i.e. the 1st coordinate, will be taken into
    account
    :rtype: (int, list)
    """

    if pos1[1] == -1 and pos1[2] != 0 \
            or pos2[1] == -1 and pos2[2] != 0:
        raise ValueError(
            "A vector of the the 3D space of positions with an edge "
            "coordinate (2nd coordinate) valued to -1 cannot have a unit "
            "coordinate higher than 0.")

    if pos1[1] not in graph[pos1[0]]:
        raise ValueError("A vector of the the 3D space of positions "
                         "cannot have an edge non connected to the "
                         "vertex of its first coordinate.")

    if pos2[1] not in graph[pos2[0]]:
        raise ValueError("A vector of the the 3D space of positions "
                         "cannot have an edge non connected to the "
                         "vertex of its first coordinate.")

    if pos1[2] == edge_lgths[pos1[1]]:
        pos1 = (target(pos1[0], pos1[1], edges_to_vertices), -1, 0)

    if pos2[2] == edge_lgths[pos2[1]]:
        pos2 = (target(pos2[0], pos2[1], edges_to_vertices), -1, 0)

    return v_dists[pos1[0]][pos2[0]]


def tc_v_to_v_path(pos1, pos2, graph: np.ndarray, edge_lgths,
                   edges_to_vertices, v_paths: list) -> \
        list:
    """
    :param pos1:
    :type pos1: 3-D tuple
    :param pos2:
    :type pos2: 3-D tuple
    :param graph:
    :type graph: 2-D iterable
    :param edge_lgths:
    :type edge_lgths: 1-D iterable
    :param edges_to_vertices:
    :type edges_to_vertices: 2-D iterable
    :param v_paths: a 3-dimensional list of all vertex-to-vertex paths
    where every path contains the vertices between the pos1's vertex (
    excluded) and the pos2's one
    :type v_paths:
    :return: the array of the path of the successive vertices in
    1-coordinate. Regardless the positions passed in parameters, only the
    vertex, i.e. the 1st coordinate, will be taken into account
    :rtype: (int, list)
    """

    if pos1[1] == -1 and pos1[2] != 0 \
            or pos2[1] == -1 and pos2[2] != 0:
        raise ValueError(
            "A vector of the the 3D space of positions with an edge "
            "coordinate (2nd coordinate) valued to -1 cannot have a unit "
            "coordinate higher than 0.")

    if pos1[1] != -1:
        if pos1[1] not in graph[pos1[0]]:
            raise ValueError("A vector of the the 3D space of positions "
                             "cannot have an edge non connected to the "
                             "vertex of its first coordinate.")

        if pos2[1] not in graph[pos2[0]]:
            raise ValueError("A vector of the the 3D space of positions "
                             "cannot have an edge non connected to the "
                             "vertex of its first coordinate.")

    if pos1[2] == edge_lgths[pos1[1]]:
        pos1 = (target(pos1[0], pos1[1], edges_to_vertices), -1, 0)

    if pos2[2] == edge_lgths[pos2[1]]:
        pos2 = (target(pos2[0], pos2[1], edges_to_vertices), -1, 0)

    return to_tc_path(pos1, pos2, v_paths[pos1[0]][pos2[0]], graph,
                      edge_lgths, edges_to_vertices)


def tc_v_to_v_paths(graph, edge_lgths, edges_to_vertices, v_paths) -> list:
    """
    :param graph:
    :type graph: 2-D iterable
    :param edge_lgths:
    :type edge_lgths: 1-D iterable
    :param edges_to_vertices:
    :type edges_to_vertices: 2-D iterable
    :param v_dists:
    :type v_dists: 2-D np.ndarray
    :param v_paths: a 3-dimensional list of all vertex-to-vertex paths
    where every path contains the vertices between the pos1's vertex (
    excluded) and the pos2's one
    :return:
    :rtype: 2-D numpy.ndarray
    """

    tc_paths = [[[] for _ in graph] for _ in graph]

    for i in range(len(graph)):
        for j in range(len(graph)):
            tc_paths[i][j] += tc_v_to_v_path((i, -1, 0), (j, -1, 0), graph,
                                             edge_lgths, edges_to_vertices,
                                             v_paths)

    return tc_paths


def tc_u_to_u_dist(pos1, pos2, graph, edge_lgths, edges_to_vertices,
                   v_dists) -> np.ndarray:
    """
    :param pos1: departure position
    :type pos1: (3,)-shaped numpy ndarray
    :param pos2: arrival position
    :type pos2: (3,)-shaped numpy ndarray
    :param graph:
    :type graph: 2-D iterable
    :param edge_lgths: an iterable of the edges's lengths of all graph
    :param edges_to_vertices: an iterable liking the edges to the vertices
    of the graph
    :param v_dists: an iterable of the distances between vertices from
    their ids.
    :return: the distancesbetween the 3-coordinate vectors pos1 and pos2. If
    pos1 is a position located on an edge leading to the vertex of pos2
    (pos2[0]) then the returned path will be empty.
    :rtype: np.ndarray
    """

    # Handling of impossible values
    if pos1[1] == -1 and pos1[2] > 0 \
            or pos2[1] == -1 and pos2[2] > 0:
        raise ValueError(
            "A vector of the the 3D space of positions with an edge "
            "coordinate (2nd coordinate) valued to -1 cannot have a unit "
            "coordinate higher than 0.")

    if pos1[1] == -1:
        pos1 = (pos1[0], graph[pos1[0]][graph[pos1[0]] > -1][0], pos1[2])
    else:
        if pos1[1] not in graph[pos1[0]]:
            raise ValueError("A vector of the the 3D space of positions "
                             "cannot have an edge non connected to the "
                             "vertex of its first coordinate.")
    if pos2[1] == -1:
        pos2 = (pos2[0], graph[pos2[0]][graph[pos2[0]] > -1][0], pos2[2])
    else:
        if pos2[1] not in graph[pos2[0]]:
            raise ValueError("A vector of the the 3D space of positions "
                             "cannot have an edge non connected to the "
                             "vertex of its first coordinate.")

    # Handling of the case where the positions are on the same edge
    if pos1[1] == pos2[1]:
        # If they are directed in the same way
        if pos1[0] == pos2[0]:
            return np.absolute(pos1[2] - pos2[2])
        # Else
        else:
            return np.absolute(pos1[2] - edge_lgths[pos2[1]] + pos2[2])

    # Marginal distance from pos1's source
    m_pos1_s = pos1[2]
    # Marginal distance from pos1's target
    m_pos1_t = edge_lgths[pos1[1]] - pos1[2]
    # Marginal distance from pos2's source
    m_pos2_s = pos2[2]
    # Marginal distance from pos2's target
    m_pos2_t = edge_lgths[pos2[1]] - pos2[2]

    pos1_t = target(pos1[0], pos1[1], graph, edges_to_vertices)
    pos2_t = target(pos2[0], pos2[1], graph, edges_to_vertices)

    # Array of transient distances to minimise
    t_dists = np.array(
        [v_dists[pos1[0]][pos2[0]] + m_pos1_s + m_pos2_s,
         v_dists[pos1[0]][pos2_t] + m_pos1_s + m_pos2_t,
         v_dists[pos1_t][pos2[0]] + m_pos1_t + m_pos2_s,
         v_dists[pos1_t][pos2_t] + m_pos1_t + m_pos2_t],
        dtype=np.int16
    )

    i = np.argmin(t_dists)

    return t_dists[i]


# 3-coordinate ( (v, e, u) ) unit-to-unit distances
def tc_u_to_u_dists(graph, edge_lgths, edges_to_vertices, v_dists) -> dict:
    tc_dists = {}

    for i in range(len(graph)):
        tc_dists[i] = {}
        for e in graph[i][graph[i] > -1]:
            tc_dists[i][e] = {}
            for u in range(edge_lgths[e]):
                tc_dists[i][e][u] = {}
                for j in range(len(graph)):
                    tc_dists[i][e][u][j] = {}
                    for f in graph[j][graph[j] > -1]:
                        tc_dists[i][e][u][j][f] = {}
                        for v in range(edge_lgths[f]):
                            tc_dists[i][e][u][j][f][v] = {}

    for i in range(len(graph)):
        for e in graph[i][graph[i] > -1]:
            for u in range(edge_lgths[e]):
                for j in range(i, len(graph)):
                    for f in graph[j][graph[j] > -1]:
                        for v in range(edge_lgths[f]):
                            tc_dists[i][e][u][j][f][v] = tc_u_to_u_dist(
                                (i, e, u), (j, f, v), graph, edge_lgths,
                                edges_to_vertices, v_dists)
                            tc_dists[j][f][v][i][e][u] = tc_u_to_u_dist(
                                (i, e, u), (j, f, v), graph, edge_lgths,
                                edges_to_vertices, v_dists)

    return tc_dists
