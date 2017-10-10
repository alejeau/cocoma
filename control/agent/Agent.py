# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017


from abc import ABC, abstractmethod
from collections import deque

import numpy as np

from control.Artifact import Artifact
from model.action.Action import Action
from model.action.Actions import Actions
from model.action.GoingToAction import GoingToAction
from model.action.MovingToAction import MovingToAction
from model.knowledge.EnvironmentKnowledge import EnvironmentKnowledge
from util.net.Connection import Connection


class Agent(ABC, Artifact):
    def __init__(self, _id: int, _original_id: str,
                 _env_knl_arg: EnvironmentKnowledge, _connection: Connection,
                 _agt_addrs: list, _depth: float = 3.0):

        Artifact.__init__(self, _connection)

        self.id = _id

        self.original_id = _original_id

        self.agt_addrs = _agt_addrs

        self.env_knl = _env_knl_arg

        self.agt_addrs = _agt_addrs

        self.current_pos = tuple(_env_knl_arg.agts_pos[self.id])

        self.goal_pos = (-1, -1, -1)

        self.DEPTH = _depth

        # Plan
        self.PLAN = deque()
        # TODO: Sending_message actions must be put on the top of the deque
        # PLAN and actions of move (type 0 et 1) on the bottom.

        self.decision = True

    def send(self, message, agt_id: int):
        super(Agent, self).send(message, self.agt_addrs[agt_id])

    # 3. Preparation of the becoming main procedure
    def prepare(self):
        self.ac = False

    # 4. Main procedure of agent

    # 4.1 Perceiving
    def perceive(self, agts_pos: np.ndarray):
        # Perceives the others agents around it
        self.env_knl.agts_pos = agts_pos

    # 4.2 Analysing
    # Analyses perceptions and received message to know its new state
    def analyse(self):
        self.receive()
        if len(self.messages) > 0:
            self.ac = False
            while len(self.messages) > 0:
                m = self.messages.popleft()
                self.process_message(m)

    # 4.2.1 Message processing
    @abstractmethod
    def process_message(self, m):
        pass

    # 4.3 Deciding
    def decide(self):
        # If this is the time to decide:
        if self.decision:
            # Applying politic defined by the strategy:
            self.strategy_decide()
        self.decision = False

    @abstractmethod
    def strategy_decide(self):
        pass

    # 4.4 Acting
    def act(self) -> Action:
        a = Action("none_action", -1)
        if len(self.PLAN) != 0:
            while not self.ac:
                a = self.PLAN.popleft()

                if a.type == Actions.Going_to:
                    self.act_gt(a)

                elif a.type == Actions.Moving_to:
                    self.act_mt(a)
                    self.ac = True

                elif a.type == Actions.Waiting:
                    self.act_w(a)
                    self.ac = True

                '''
                elif a.type == Actions.Stopping_move:
                    self.act_st_mv(a)
                '''
        return a

    # Act going to
    def act_gt(self, a: GoingToAction):
        print(str(self.id), "is in", self.current_pos,
              " and planned to go to ", a.goal_position)

        # Retrieval of the path from current_pos to goal_vertex
        path = self.env_knl.space.path(self.current_pos,
                                       a.goal_position)

        self.goal_pos = a.goal_position
        # Making up of the plan of Moving_to actions to go to
        # goal_vertex
        print(str(self.id), " takes the path: ", path)
        for i in range(len(path) - 1):
            self.PLAN.append(MovingToAction(path[i], path[i + 1]))

    # Act moving to
    def act_mt(self, a: MovingToAction):
        print(str(self.id), "is in", self.current_pos,
              " and planned to move to ", a._to)

        self.current_pos = a._to

        if self.goal_pos == a._to:
            # misc.vertices_equals(self.goal_pos, a._to)
            self.decision = True

    # Act waiting
    def act_w(self, a: Action):
        pass

    # Act stopping move
    def act_st_mv(self, a: Action):
        for i in range(len(self.PLAN)):
            # Deletion of the actions being Going/Moving_to
            # actions
            if self.PLAN[i].type < 2:
                del self.PLAN[i]

    def reset_idl(self, p: tuple):
        """
        :param p: idleness' position to reset into in a 3D vector (v, e, u)
        :type p: tuple
        :return:
        :rtype:
        """
        self.env_knl.idls[p[0]] = 0

    # 5 Knowledge Processing
    def update_knowledge(self):
        self.env_knl.tick()

        # If the agent is on a vertex and is not crossing an edge
        if self.current_pos[1] == -1:
            self.reset_idl(self.current_pos)
