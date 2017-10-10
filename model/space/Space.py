# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

import numpy as np

import util.spaceprocessor as sp


class Space:
    def __init__(self, _graph: np.ndarray, _edges_to_vertices: np.ndarray,
                 _edge_lgths: np.ndarray, _edge_activations, _locations:
            np.ndarray):

        self.graph = _graph

        self.edges_to_vertices = _edges_to_vertices

        self.edge_lgths = _edge_lgths

        self.max_units_of_edge = self.edge_lgths.max()

        self.locations = _locations

        self.edge_activations = np.array(_edge_activations, dtype=np.int16)

        # Neighbours, distances and paths
        self.ngbrs = sp.build_tc_neighbours(self.graph)

        # dists = sp.tc_u_to_u_dists(self.graph, edge_lgths,
        # edges_to_vertices, v_dists)
        self.dists = {}
        self.v_dists, self.v_paths = sp.fw_distances(_graph, _edge_lgths)
        self.paths = sp.tc_v_to_v_paths(_graph, _edge_lgths,
                                              _edges_to_vertices, self.v_paths)

    def target(self, s: int, e: int) -> int:
        """
        :param s: the source whose the edge is stemmed from
        :type s: int
        :param e: the edge whose the target is requested
        :type e: int
        :return:
        :rtype: int
        """
        return sp.target(s, e, self.edges_to_vertices)

    def target(self, pos: tuple) -> int:
        """
        :param pos:
        :type pos:
        :return:
        :rtype: int
        """
        return self.target(pos[0], pos[1])

    def edge(self, v0: int, v1: int) -> int:
        return sp.edge(v0, v1, self.graph)

    def edge(self, vertices: np.ndarray) -> int:
        return self.edge(vertices[0], vertices[1])

    """"
    def dist(self, pos1: tuple, pos2: tuple) -> int:
        if pos1[1] == -1:
            pos1 = (pos1[0], self.graph[pos1[0]][self.graph[pos1[0]] > -1][0],
                    pos1[2])
        if pos2[1] == -1:
            pos2 = (pos2[0], self.graph[pos2[0]][self.graph[pos2[0]] > -1][0],
                    pos2[2])

        return self.dists[pos1[0]][pos1[1]][pos1[2]][pos2[0]][pos2[1]][pos2[2]]
    """

    def dist(self, pos1: tuple, pos2: tuple) -> int:
        return self.v_dists[pos1[0]][pos2[0]]

    def path(self, pos1: tuple, pos2: tuple) -> list:
        """
        :param pos1:
        :type pos1:
        :param pos2:
        :type pos2:
        :return:
        :rtype:
        """

        if pos1[1] == -1 and pos1[2] != 0 \
                or pos2[1] == -1 and pos2[2] != 0:
            raise ValueError(
                "A vector of the the 3D space of positions with an edge "
                "coordinate (2nd coordinate) valued to -1 cannot have a unit "
                "coordinate higher than 0.")

        if pos1[1] == -1:
            pos1 = (pos1[0], self.graph[pos1[0]][self.graph[pos1[0]] > -1][0],
                    pos1[2])
        else:
            if pos1[1] not in self.graph[pos1[0]]:
                raise ValueError("A vector of the the 3D space of positions "
                                 "cannot have an edge non connected to the "
                                 "vertex of its first coordinate.")
        if pos2[1] == -1:
            pos2 = (pos2[0], self.graph[pos2[0]][self.graph[pos2[0]] > -1][
                0], pos2[2])
        else:
            if pos2[1] not in self.graph[pos2[0]]:
                raise ValueError("A vector of the the 3D space of positions "
                                 "cannot have an edge non connected to the "
                                 "vertex of its first coordinate.")

        return self.paths[pos1[0]][pos2[0]]

    def neighbours(self, p: tuple) -> list:
        """
        :param p: the position as a 3D vector
        :type p: tuple
        :return:
        :rtype:
        """
        return self.ngbrs[p[0]]

