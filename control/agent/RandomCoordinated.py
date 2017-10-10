# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

from control.agent.Coordinated import Coordinated
from model.knowledge.EnvironmentKnowledge import EnvironmentKnowledge
from util.net.Connection import Connection


class RandomCoordinated(Coordinated):

    def __init__(self, _id: int, _original_id: str,
                 _env_knl_arg: EnvironmentKnowledge, _connection: Connection,
                 _agt_addrs: list):

        Coordinated.__init__(self, _id, _original_id, _env_knl_arg,
                             _connection,
                       _agt_addrs)

    def strategy_decide(self):
        self.send("position_request:" + str(self.id) + ":" + str(
                  self.current_pos), 0)
