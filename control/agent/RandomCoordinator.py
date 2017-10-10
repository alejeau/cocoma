# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

import numpy as np

from control.agent.Coordinator import Coordinator
from model.knowledge.EnvironmentKnowledge import EnvironmentKnowledge
from util.net.Connection import Connection


class RandomCoordinator(Coordinator):

    def __init__(self, _id: int, _original_id: str,
                 _env_knl_arg: EnvironmentKnowledge, _connection: Connection,
                 _agt_addrs: list):

        Coordinator.__init__(self, _id, _original_id, _env_knl_arg,
                             _connection,
                       _agt_addrs)

        self.decision = False

    def strategy_decide(self):
        while len(self.to_send) > 0:
            # For each entry e in the list of dictionaries to_send
            e = self.to_send.popleft()

            i = np.random.randint(len(self.env_knl.space.neighbours(
                e["pos"])))

            self.send("goal_position:" + str(self.env_knl.space.neighbours(
                e["pos"])[i]), e["a_id"])