import numpy as np

from ast import literal_eval as make_tuple

from control.agent.Agent import Agent
from model.action.GoingToAction import GoingToAction
from model.knowledge.EnvironmentKnowledge import EnvironmentKnowledge
from util.net.Connection import Connection


class RandCoordinated(Agent):

    def __init__(self, _id: int, _original_id: str,
                 _env_knl_arg: EnvironmentKnowledge, _connection: Connection,
                 _agt_addrs: list):
        Agent.__init__(self, _id, _original_id, _env_knl_arg, _connection,
                       _agt_addrs)

    def process_message(self, m):
        if str(m).startswith("goal_position"):
            # Split string
            ss = str(m).split(':')
            self.PLAN.append(GoingToAction(make_tuple(ss[1])))

    def strategy_decide(self):
        self.send("position_request:" + str(self.id) + ":" + str(self.current_pos), 0)


