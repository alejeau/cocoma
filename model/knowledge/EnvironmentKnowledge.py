# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017


# Environment = topology (map) + society

import numpy as np
import util.miscellaneous as misc
from model.space.Space import Space


class EnvironmentKnowledge:
    def __init__(self, _space: Space, _idls: np.ndarray, _speeds: dict,
                 _agts_pos: np.ndarray):
        """
        :param space:
        :type space:
        :param idls:
        :type idls:
        :param speeds:
        :type speeds:
        :param agts_pos: A ndarray which contains the known positions of
        the agents. A position is defined as a 3-element array : [<vertex>,
        <edge>, <unit of edge>]. The default values of <edge> and <unit of
        edge> are -1 and 0, respectively (agent is not travelling any edge).
        :type agts_pos: numpy.ndarray
        """

        # Space
        self.space = _space
        self.idls = np.array(_idls, np.int16)
        self.speeds = _speeds

        # Time
        self.t = 0

        # Society

        #
        # Individual perception of the others agents' position
        self.agts_pos = _agts_pos
        # self.dists_to_agts = self.space.compute_dists_to_agts(self.agt_id,
        # self.space, self.agts_pos)

        self.vertices_to_agents = \
            np.ones(len(self.space.graph), np.int16) * (-1)
        self.edges_to_agents = \
            np.ones(len(self.space.graph), np.int16) * (-1)

        for i in range(len(self.agts_pos)):
            self.vertices_to_agents[self.agts_pos[i][0]] = i
            # TODO: set an array for probabilities of edges or other

    def tick(self):
        self.t += 1
        self.idls += 1

    def target(self, agt_id: int):
        return self.space.target(self.agts_pos[agt_id])
