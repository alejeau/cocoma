# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017


# In ancient Greek religion, the goddess Ananke is a personification of
# inevitability, compulsion and necessity. She is often depicted as holding
# a spindle.

import pickle
from pprint import pprint

import numpy as np

import util.miscellaneous as misc
from control.Artifact import Artifact
from control.agent.Agent import Agent
from model.AgentTypes import AgentTypes
from model.Data import Data
from model.action.Action import Action
from model.action.Actions import Actions
from model.knowledge.EnvironmentKnowledge import EnvironmentKnowledge
from model.space.Space import Space
from util.SimPreprocessor import SimPreprocessor
from util.net.Connection import Connection
from util.net.SimulatedConnection import SimulatedConnection


class Ananke(Artifact):
    def __init__(self, _cnn: Connection, _config_path: str, _archivist_addr,
                 _cycle_number: int, _depth: float):
        Artifact.__init__(self, _cnn)

        self.cycles_number = _cycle_number
        self.t = 0
        self.display_addr = None
        self.archivist_addr = _archivist_addr
        self.depth = _depth

        # I. Configuration

        # I.1. Environment

        # I.1.1. Space initialisation
        config_path = _config_path

        self.graph, fl_edge_lgths, edges_to_vertices, locations, \
        edge_activations, idls, socs, societies_speeds, \
        societies_agts_pos = SimPreprocessor.load_config(config_path)

        edge_lgths = np.array(np.round(fl_edge_lgths), dtype=np.int16)

        for s in societies_speeds:
            if s["id"] != "InactiveSociety":
                self.speeds = s["speeds"]

        self.space = Space(self.graph, edges_to_vertices, edge_lgths,
                           edge_activations, locations)

        # I.1.3. Idlenesses
        self.idls = idls

        # I.2. Agents

        # I.2.2. Agent generation
        self.agt_addrs, self.agts_pos = self.load_societies(socs,
                                                            self.space,
                                                            idls,
                                                            self.speeds,
                                                            societies_agts_pos)

        # Raising an exception if forbidden values are set
        if len(self.agts_pos[self.agts_pos[:, 2] < 0]) > 0:
            raise ValueError("Negative unit of edge forbidden")

        no_edge_agts_pos = self.agts_pos[self.agts_pos[:, 1] < 0]
        if len(no_edge_agts_pos[no_edge_agts_pos[:, 2] > 0]) > 0:
            raise ValueError("Forbidden value(s) for the position("
                             "s) ", no_edge_agts_pos[no_edge_agts_pos[:,
                                                     2] > 0], "of agts_pos. "
                                                              "Units non "
                                                              "equal to zero "
                                                              "with no edge "
                                                              "(-1) impossible"
                             )

        # I.2.3. Archivist
        # archivist = Archivist(env_knl, self.agt_addrs)

        if self.display_addr is not None:
            # Sending of the graph to the GUI
            graph_p = pickle.dumps(self.graph)
            edge_lgths_p = pickle.dumps(edge_lgths)
            self.send(graph_p, self.display_addr)
            self.send(edge_lgths_p, self.display_addr)

    def run(self):
        print("Ananke: starts")

        while not self.stop_working:
            # Creation of the Completed List which is a dictionary
            c_list = {}

            while self.t < self.cycles_number:
                print("\nCycle ", self.t, ':')

                self.send_to_archivist()

                for i in range(len(self.agt_addrs)):
                    c_list[i] = 1

                for a in self.agt_addrs:
                    a.prepare()

                for a in self.agt_addrs:
                    # Broadcast of the perceptions to the agents
                    agts_pos = self.build_agts_pos(a)
                    # subgraph = self.build_subgraph(a)
                    # current_pos = self.build_current_vertex(a)
                    a.perceive(agts_pos)

                while len(c_list) != 0:
                    # Main procedure of agents
                    for a in self.agt_addrs:
                        a.analyse()
                    for a in self.agt_addrs:
                        a.decide()
                    for a in self.agt_addrs:
                        action = a.act()  # After each act() operation,
                        # the agent have to activate its attribute ac
                        self.process_action(action, a)

                    # The coordinator agent is a special type of agent. Its
                    # "action completed" boolean variable noted ac is always
                    #  true because it executes no action but just sends and
                    #  receives messages
                    if self.agt_addrs[0].original_id == "coordinator":
                        self.agt_addrs[0].ac = True

                    for a in self.agt_addrs:
                        # Testing if a change have to be done on the Completed
                        # List
                        if a.ac and a.id in c_list:
                            del c_list[a.id]
                        elif not a.ac and a.id not in c_list:
                                c_list[a.id] = 1

                print("Global idlenesses ", self.idls)

                for a in self.agt_addrs:
                    a.update_knowledge()

                self.update_environment()

            if self.display_addr is not None:
                self.send("stop_working", self.display_addr)

            self.archivist_addr.save_log()
            self.stop_working = True

            print("Ananke: stops to work")

    def build_agts_pos(self, a: Agent) -> np.ndarray:
        # Agents' distance from a
        # a_agts_dists = misc.compute_dists_to_agts(a.id, self.agts_pos,
        # self.space)

        a_agts_dists = misc.former_compute_dists_to_agts(a.id,
                                                         self.agts_pos,
                                                         self.graph,
                                                         self.space.edge_lgths,
                                                         self.space.edges_to_vertices,
                                                         self.space.v_dists)

        # print("Ananke.build_agts_pos: ", a_agts_dists)

        # Positions of agents perceived by a
        a_agts_pos = np.array(self.agts_pos, dtype=np.int16) * -1

        for i in range(len(self.agts_pos)):
            if a_agts_dists[i] <= a.DEPTH:
                # TODO : That bellow evaluation enables to disconnect the
                # circuit of the self perceiving, a reference is passed  To
                # be tested.
                a_agts_pos[i] = self.agts_pos[i]

        return a_agts_pos

    def build_subgraph(self, a: Agent):
        return self.graph

    def build_current_vertex(self, a: Agent):
        return self.agts_pos[a.id]

    def process_action(self, action: Action, a: Agent):
        if action.type == Actions.Moving_to:
            if not np.array_equal(self.agts_pos[a.id], action._from):
                print(self.agts_pos[a.id], action._from)
                raise ValueError(
                    "Inconsistent start vertex in this MovingTo "
                    "Action")

            self.agts_pos[a.id] = action._to

            if self.display_addr is not None:
                self.send(pickle.dumps(self.agts_pos[a.id]), self.display_addr)

    def update_environment(self):
        self.t += 1
        self.idls += 1

        for a in self.agt_addrs:
            self.idls = np.where(a.env_knl.idls < self.idls,
                                 a.env_knl.idls, self.idls)

    def load_societies(self, socs: dict, space: Space, idls: np.ndarray,
                       speeds: np.ndarray, societies_agts_pos: dict) -> (
                                                             list, np.ndarray):
        agt_addrs = []
        env_knl = None
        agts_pos = np.empty([0, 3], dtype=np.int16)
        # I.2.1. Agent Position
        # Initial agents positions
        for s in societies_agts_pos:
            if s["id"] != "InactiveSociety":
                agts_pos = s["agts_pos"]

        # TODO: Fulfill env_knl.vertices_to_agents and
        # env_knl.edges_to_agents with -1 before updating it

        for s in socs:
            if s["id"] != "InactiveSociety":
                for a in s['agents']:
                    # Here all agents and Ananke share the same space object
                    #  in order to accelerate the initialisation
                    env_knl = EnvironmentKnowledge(space, idls.copy(),
                                                   speeds.copy(),
                                                   agts_pos.copy())
                    cnn = SimulatedConnection()

                    # Agents
                    # Initializing agents, retrieving their address to put them
                    #  into a list to send it to the archivist. In order to
                    #  keep idlenesses and agents position personal, passing
                    #  graph and agent perception by copy except for the
                    #  archivist

                    a = AgentTypes.id_to_class_name[a["type"]](a["id"],
                                                               a["original_id"],
                                                               env_knl, cnn,
                                                               agt_addrs)


                    agt_addrs.append(a)

                for a in agt_addrs:
                    a.agt_addrs = agt_addrs

        return agt_addrs, agts_pos

    def send_to_archivist(self, agts_pos: np.ndarray, idls: np.ndarray):
        self.send(pickle.dumps({Data.Cycle: self.t, Data.Agts_pos:
            agts_pos.tolist(), Data.Idls: idls.tolist()}),
                  self.archivist_addr)

    def send_to_archivist(self):
        self.archivist_addr.log(self.t, self.agts_pos.tolist(),
                                self.idls.tolist())
