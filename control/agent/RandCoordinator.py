import numpy as np

from ast import literal_eval as make_tuple
from collections import deque

from control.agent.Agent import Agent
from model.knowledge.EnvironmentKnowledge import EnvironmentKnowledge
from util.net.Connection import Connection


class RandCoordinator(Agent):

    def __init__(self, _id: int, _original_id: str,
                 _env_knl_arg: EnvironmentKnowledge, _connection: Connection,
                 _agt_addrs: list):

        Agent.__init__(self, _id, _original_id, _env_knl_arg, _connection,
                       _agt_addrs)

        # Messages to send to the agents to provide them their next goal
        # position
        self.to_send = deque()

    def process_message(self, m):
        if str(m).startswith("position_request"):
            # Split string
            ss = str(m).split(':')
            self.to_send.append({"a_id": int(ss[1]), "pos": make_tuple(ss[2])})

            self.decision = True

    def strategy_decide(self):
        while len(self.to_send) > 0:
            # For each entry e in the list of dictionaries to_send
            e = self.to_send.popleft()

            i = np.random.randint(len(self.env_knl.space.neighbours(e["pos"])))

            self.send("goal_position:" + str(self.env_knl.space.neighbours(e["pos"])[i]), e["a_id"])

