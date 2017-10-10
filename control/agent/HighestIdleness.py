import numpy as np

from control.agent.Agent import Agent
from model.action.GoingToAction import GoingToAction
from model.knowledge.EnvironmentKnowledge import EnvironmentKnowledge
from util.net.Connection import Connection


class HighestIdleness(Agent):

    def __init__(self, _id: int, _original_id: str,
                 _env_knl_arg: EnvironmentKnowledge, _connection: Connection,
                 _agt_addrs: list):
        Agent.__init__(self, _id, _original_id, _env_knl_arg, _connection,
                       _agt_addrs)

    def analyse(self):
        pass

    # not so random reaction:
    # check idleness from surrounding nodes and go to the highest one
    def strategy_decide(self):
        # we get the list of neighbours
        neighbours = self.env_knl.space.neighbours(self.current_pos)

        max_idls = -2 # idleness max
        idx_max = -2  # index of the max idleness

        for n in range(len(neighbours)):
            idlss = self.env_knl.idls[neighbours[n][0]]
            # print(idx_max, neighbours)
            # print(idlss,self.env_knl.idls)
            # if idleness is superior to the current max, we update
            if (idlss > max_idls):
                max_idls = idlss
                idx_max = n

        # once the highest idleness found, we set plan to go there
        self.PLAN.append(GoingToAction(neighbours[idx_max]))

    def process_message(self, m):
        pass


