import numpy as np
import sys

from ast import literal_eval as make_tuple
from collections import deque

from control.agent.Agent import Agent
from model.knowledge.EnvironmentKnowledge import EnvironmentKnowledge
from model.space.Space import Space
from util.net.Connection import Connection


class HpccCoordinator(Agent):

    def __init__(self, _id: int, _original_id: str,
                 _env_knl_arg: EnvironmentKnowledge, _connection: Connection,
                 _agt_addrs: list):

        Agent.__init__(self, _id, _original_id, _env_knl_arg, _connection,
                       _agt_addrs)

        # Messages to send to the agents to provide them their next goal
        # position
        self.to_send = deque()

    # param r
    r = 0.5

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

            print("e: " + str(e))

            # voisins de e
            neighbours = self.env_knl.space.neighbours(e["pos"])

            self.norm_idlnss(e["pos"], neighbours)

            i = np.random.randint(len(self.env_knl.space.neighbours(e["pos"])))

            self.send("goal_position:" + str(self.env_knl.space.neighbours(e["pos"])[i]), e["a_id"])

    # Oisiveté normalisée
    def norm_idlnss(self, v, neighbours) :
        # print("neighbours: " + str(neighbours))
        dist_max = -1
        dist_min = sys.maxsize # biggest practical int

        for n in neighbours:
            print("v: " + str(v))
            print("n: " + str(n))
            print(str(Space.dist(v, n)))
            dist = Space.edge(v, n)
            if dist > dist_max:
                dist_max = dist
            elif dist < dist_min:
                dist_min = dist

        idlnss = self.env_knl.idls
        print(idlnss)

        pass

    # Time to go normalisé
    def norm_ttg(self, v, neighbours):

        pass