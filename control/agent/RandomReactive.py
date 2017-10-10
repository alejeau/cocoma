import numpy as np

from control.agent.Agent import Agent
from model.action.GoingToAction import GoingToAction
from model.knowledge.EnvironmentKnowledge import EnvironmentKnowledge
from util.net.Connection import Connection


class RandomReactive(Agent):

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
        i = np.random.randint(len(self.env_knl.space.neighbours(self.current_pos)))

        self.PLAN.append(GoingToAction(self.env_knl.space.neighbours(
            self.current_pos)[i]))

        # i = np.random.randint(len(self.env_knl.space.graph[
        # self.current_pos[0]]))
        # self.PLAN.append(GoingToAction((i, -1, 0)))


    def process_message(self, m):
        pass


