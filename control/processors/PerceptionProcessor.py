# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

from collections import deque
import numpy as np

from model.knowledge.EnvironmentKnowledge import EnvironmentKnowledge
from model.perception.AgentsPerception import AgentsPerception
from model.perception.GraphPerception import GraphPerception
from model.perception.Perceptions import Perceptions
from model.perception.SelfPerception import SelfPerception


class PerceptionProcessor:

    def process(self, pcps: deque, current_pos: np.ndarray, env_knl:
    EnvironmentKnowledge):
        for p in pcps:
            if p.type == Perceptions.Self:
                self.process_self_pcp(p, current_pos)
            elif p.type == Perceptions.Agents:
                self.process_agts_pcp(p, env_knl)
            else:
                self.process_graph_pcp(p, env_knl)

    @staticmethod
    def process_self_pcp(p: SelfPerception, current_pos : np.ndarray):
        current_pos[:] = p.pos[:]

    @staticmethod
    def process_agts_pcp(p: AgentsPerception, env_knl: EnvironmentKnowledge):
        env_knl.agts_pos = p.agts_pos

    @staticmethod
    def process_graph_pcp(p: GraphPerception, env_knl: EnvironmentKnowledge):
        env_knl.space.graph = p.graph
        env_knl.space.edge_activations = p.edge_activations
