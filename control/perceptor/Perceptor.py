# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

from collections import deque
import numpy as np

from model.perception.GraphPerception import GraphPerception
from model.perception.SelfPerception import SelfPerception
from model.perception.AgentsPerception import AgentsPerception


class Perceptor():
    def __init__(self, depth_arg : int,):
        # self.perceptions = perceptions_arg

        # Depth parameter
        self.DEPTH = depth_arg

    @staticmethod
    def perceive_agts(perceived_agts_pos : np.ndarray) -> \
            AgentsPerception:
        """
        :param perceived_agts_pos:
        :type perceived_agts_pos:
        :return:
        :rtype:
        """
        # The perceived_agts_pos argument are provided by the simulator
        return AgentsPerception(perceived_agts_pos)

    @staticmethod
    def perceive_graph(subgraph : np.ndarray) -> GraphPerception:
        return GraphPerception(subgraph, [])

    @staticmethod
    def perceive_self(current_pos : np.ndarray) -> SelfPerception:
        """
        :param current_pos: a 3-shape ndarray [vertex, edge, unit of edge]
        :type current_pos: numpy.ndarray
        :return: a self perception
        :rtype: SelfPerception
        """
        return SelfPerception(current_pos)

    def post_perception(self, agts_pos, subgraph, current_pos, pcps : deque):
        pcps.append(self.perceive_self(current_pos))
        pcps.append(self.perceive_agts(agts_pos))
        pcps.append(self.perceive_graph(subgraph))
