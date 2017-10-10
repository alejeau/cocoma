# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

import random
from pprint import pprint

import untangle
import json
import numpy as np
import os

import util.miscellaneous as misc
from model.AgentTypes import AgentTypes
from model.Maps import Maps


class SimPreprocessor:
    @classmethod
    def load_config(cls, file_path: str):
        if file_path.endswith("xml"):
            return cls.config_xml_to_iterables(file_path)
        elif file_path.endswith("json"):
            with open(file_path) as file:
                return cls.config_dict_to_iterables(json.load(file))
        else:
            raise ValueError("Only JSON and XML files can be loaded.")

    @classmethod
    def generate_configs(cls, ms: list, agts_nbss: list = None,
                         mats: list = None, cdtrss: list = None,
                         mns: list = None, sns: list = None,
                         execs_nb: int = 10, dp: str = ''):
        """
        :param ms: map ids
        :type ms: list
        :param dp: output directory path
        :type dp: str
        :param agts_nbss:
        :type agts_nbss:
        :param mns: meta-societies' names
        :type mns:
        :param sns: societies' names for each metasociety
        :type sns: list
        :param mats: meta-societies agents types: type of agents for each
        metasociety and for each society within this meta-society. Each
        element along the 1st dimension corresponds to a meta-society and each
        element along the 2nd dimension corresponds to a society
        :type mats:
        :param cdtrss: presence of a coordinator for every society in each
        meta-society
        :type cdtrss: 2D list of bool
        :param execs_nb:
        :type execs_nb:
        :return:
        :rtype:
        """
        if agts_nbss is None:
            agts_nbss = [[]]
        if mats is None:
            mats = [[[]]]
        if mns is None:
            mns = []
            for i in range(len(agts_nbss)):
                # Each i represents the id of the current bunch of numbers
                # of agents numbers i.e. the current meta-society
                mns += [misc.name_society(agts_nbss[i], str(i))]
        if sns is None:
            sns = []
            for i in range(len(agts_nbss)):
                sn = []
                for j in range(len(agts_nbss[i])):
                    sn += [misc.name_society([agts_nbss[i][j]], str(j))]
                sns += [sn]

        if len(agts_nbss) != len(mats):
            raise ValueError(
                "The number of meta-societies in the mats list must "
                "be equal to the bunches of numbers of agents numbers in "
                "agts_nbss list")

        # The same population size ids: a list that gather the ids of mats
        # which have the same population size for their societies, for each
        # societies coupling (under a meta-society)
        sps_ids = misc.rtrv_sm_v_in_itr(agts_nbss)
        for m in ms:
            for e in range(execs_nb):
                for ids in sps_ids:
                    # Number of agents in all societies of the current
                    # meta-society
                    an = sum(agts_nbss[ids[0]])

                    graph = cls.load_map(m)

                    # Vertices to the dict format randomly selected on which
                    # agents will stand
                    vs = random.sample([v["id"] for v in graph["vertices"]],
                                       an)

                    for i in ids:
                        # Generation of a blank configuration structured for
                        #  the mats whose indices are in the ids list
                        config, op = cls.generate_blank_config(m,
                                                               agts_nbss[i],
                                                               mats[i],
                                                               cdtrss[i],
                                                               mns[i],
                                                               dp=dp)

                        # List of dict vertices
                        exc = cls.inject_agts_positions_in_config(config, vs)

                        op = op.replace("blank", str(e))

                        with open(op, 'w') as s:
                            # s as stream
                            json.dump(exc, s)

                        print(op, " generated.")

    @classmethod
    def generate_blank_config(cls, m: int, agts_nbs: list = None,
                              sats: list = None, cdtrs: list = None,
                              mn: str = '', sn: list = None,
                              op: str = '', sp: str = None, dp: str = '') ->\
            (dict, str):
        """
        Generates a blank simulation configuration file i.e. a config where
        agents have no positions

        :param dp:
        :type dp:
        :param m: the map id. See model.Maps
        :type m: int
        :param sp: societies file path
        :type sp: str
        :param agts_nbs: agent number for each society
        :type agts_nbs: list
        :param mn: metasociety name
        :type mn: str
        :param sn: societies' names
        :type sn:
        :param cdtrs:
        :type cdtrs:
        :param sats: societies agents types: type of agents for each society.
        Each element of the 1st dimension corresponds to a society
        :type sats: 2D list
        :param op:
        :type op:
        :param dp:
        :type dp:
        :return: the path of the generated file
        :rtype:
        """
        if agts_nbs is None:
            agts_nbs = []

        if op == "":
            op = misc.name_config_file(m, agts_nbs, sats, mn, sfx="blank",
                                       dp=dp)

        config = {"environment": {"graph": cls.load_map(m)}}

        if sp is not None:
            # TODO: take into account the case where a config file of the
            # society is provided
            pass
        else:
            config["environment"]["meta-society"] = {"id": mn,
                                                     "societies":
                                                        cls.generate_societies(
                                                             agts_nbs, sats,
                                                             cdtrs, sn, op)
                                                     }

        directory = os.path.dirname(op)
        if not os.path.exists(directory):
            os.makedirs(directory)

        return config, op

    @staticmethod
    def load_map(m: int):
        with open(Maps.id_to_path[m]) as s:
            return json.load(s)

    @staticmethod
    def generate_societies(agts_nbs: list = None, sats: list = None,
                           cdtrs: list = None, sn: list = None, op: str = ""):
        if agts_nbs is None:
            agts_nbs = []
        if sats is None:
            sats = [[]]
        if cdtrs is None:
            cdtrs = [False] * len(agts_nbs)
        if sn is None:
            sn = []
            for i in range(len(agts_nbs)):
                sn += [misc.name_society([agts_nbs[i]], str(i))]

        if len(agts_nbs) != len(sn):
            raise ValueError("The number of society names in the sn list "
                             "must be equal to the number of agents numbers "
                             "in the agts_nbs list")
        if len(agts_nbs) != len(sats):
            raise ValueError("The number of societies in the sats list must "
                             "be equal to the number of agents numbers in "
                             "agts_nbs list")
        for i in range(len(agts_nbs)):
            if 1 < len(sats[i]) != agts_nbs[i]:
                raise ValueError("Each number of types in the sats 2D list "
                                 "must be equals to the corresponding number "
                                 "of agents in the agts_nbs list")
            if len(sats[i]) == 1:
                sats[i] = sats[i] * agts_nbs[i]

        socs = []
        for i in range(len(agts_nbs)):
            soc = {"id": sn[i], "label": sn[i], "is_closed": "true"}
            agts = []

            if cdtrs[i]:
                agts += [{"id": "coordinator", "type": sats[i][0],
                          "vertex_id": ""}]
            else:
                agts += [{"id": "0", "type": sats[i][0],
                          "vertex_id": ""}]

            for j in range(1, agts_nbs[i]):
                agts += [{"id": str(j), "type": sats[i][j], "vertex_id": ""}]

            soc["agents"] = agts
            socs += [soc]

        if op != "":
            pass

        return socs

    @classmethod
    def inject_agts_positions_in_config(cls, config: dict, vs: list) -> dict:
        """
        :param config:
        :type config:
        :param vs: vertices
        :type vs: dict
        :return:
        :rtype:
        """

        new_config = {**config}

        # Next vertice from the vs list to insert
        nv = 0
        for s in new_config["environment"]["meta-society"]["societies"]:
            cls.inject_agts_positions_in_soc(s, vs[nv:nv + len(s["agents"])])
            nv = len(s["agents"])

        return new_config

    @staticmethod
    def inject_agts_positions_in_soc(soc: dict, vs: list):
        for i in range(len(soc["agents"])):
            soc["agents"][i]["vertex_id"] = vs[i]

    @staticmethod
    def generate_config():
        pass

    @classmethod
    def convert_config_xml_to_json(cls, xml_path: str, json_path: str):
        with open(json_path, 'w') as s:
            # s as stream
            json.dump(cls.config_xml_to_dict(xml_path), s)

    @classmethod
    def convert_map_xml_to_json(cls, xml_path: str, json_path: str):
        with open(json_path, 'w') as s:
            # s as stream
            json.dump(cls.map_xml_to_dict(xml_path), s)

    @classmethod
    def convert_socs_xml_to_json(cls, xml_path: str, json_path: str):
        with open(json_path, 'w') as s:
            # s as stream
            json.dump(cls.socs_xml_to_dict(xml_path), s)

    @classmethod
    def config_xml_to_dict(cls, path: str):
        agt_type = path.split("/")
        agt_type = agt_type[len(agt_type) - 1].split("-")[0]
        doc = untangle.parse(path)
        return cls.config_untangle_to_dict(doc, agt_type)

    @classmethod
    def map_xml_to_dict(cls, path: str):
        doc = untangle.parse(path)
        return cls.map_untangle_to_dict(doc)

    @classmethod
    def socs_xml_to_dict(cls, path: str):
        agt_type = path.split("/")
        agt_type = agt_type[len(agt_type) - 1].split("-")[0]
        doc = untangle.parse(path)
        return cls.socs_untangle_to_dict(doc)

    @staticmethod
    def map_dict_to_iterables(d: dict):
        vertices = {}

        vertices_d = d['environment']['graph']['vertices']
        i = 0
        for n in vertices_d:
            vertices[n['id']] = i
            i += 1

        edges_d = d['environment']['graph']['edges']
        graph = np.ones([len(vertices), len(vertices)], dtype=np.int16) * -1

        # Floating edge lengths
        fl_edge_lgths = np.zeros([len(edges_d)], dtype=np.float16)
        i = 0
        for e in edges_d:
            graph[vertices[e['source']]][vertices[e['target']]] = i
            graph[vertices[e['target']]][vertices[e['source']]] = i
            fl_edge_lgths[i] = float(e['length'])
            i += 1

        edges_to_vertices = np.empty([len(fl_edge_lgths), 2], dtype=np.int16)
        for i in range(len(graph)):
            # Retrieval of the existing edges' indices ( > -1) in the column
            #  of the edges of i
            for j in np.argwhere(graph[i] > -1):
                edges_to_vertices[graph[i][j]] = [i, j]

        locations = np.array([], np.float32)

        edge_activations = np.ones(len(fl_edge_lgths), dtype=np.int16)

        idls = np.array([0] * len(graph), dtype=np.int16)

        return vertices, graph, fl_edge_lgths, edges_to_vertices, locations, \
               edge_activations, idls

    @classmethod
    def socs_dict_to_iterables(cls, d: dict) -> tuple:
        vertices = cls.map_dict_to_iterables(d)[0]

        socs_d = d["environment"]["meta-society"]["societies"]
        socs = []
        societies_speeds = []
        societies_agts_pos = []
        for soc_d in socs_d:
            s = {"id": soc_d["id"], "agents": []}
            speeds = np.empty([0], dtype=np.float16)
            agts_pos = np.empty([0, 3], dtype=np.int16)
            i = 0

            # Testing if the position of agents in the society is defined
            pos_def = True
            if len(soc_d["agents"]) != 0:
                if soc_d["agents"][0]["vertex_id"] == "" \
                        or soc_d["agents"][0]["vertex_id"] == "a" \
                        or soc_d["agents"][0]["vertex_id"] == "c":
                    pos_def = False

            for j in range(len(soc_d["agents"])):
                if soc_d["agents"][i]["id"] == "coordinator":
                    buffer = soc_d["agents"][0]
                    soc_d["agents"][0] = soc_d["agents"][i]
                    soc_d["agents"][i] = buffer
                    break

            for agt_dic in soc_d["agents"]:
                a = {"id": i, "original_id": agt_dic["id"],
                     "type": AgentTypes.str_to_id[agt_dic["type"]],
                     "vertex_id": vertices[agt_dic["vertex_id"]] if
                     pos_def else -1}

                s["agents"].append(a)
                speeds = np.append(speeds, [1], axis=0)
                agts_pos = np.append(agts_pos, [[vertices[agt_dic[
                    "vertex_id"]], -1, 0]], axis=0)
                i += 1

            societies_speeds.append({"id": s["id"], "speeds": speeds})
            societies_agts_pos.append({"id": s["id"], "agts_pos": agts_pos})
            socs.append(s)

        return socs, societies_speeds, societies_agts_pos

    @classmethod
    def config_dict_to_iterables(cls, d: dict) -> tuple:
        vertices, graph, fl_edge_lgths, edges_to_vertices, locations, \
        edge_activations, idls = cls.map_dict_to_iterables(d)

        socs, societies_speeds, societies_agts_pos = \
            cls.socs_dict_to_iterables(d)

        return graph, fl_edge_lgths, edges_to_vertices, locations, \
               edge_activations, idls, socs, societies_speeds, \
               societies_agts_pos

    @staticmethod
    def map_untangle_to_dict(doc: untangle.Element):
        graph = {'label': doc.graph['label'], 'vertices': []}

        for n in doc.graph.node:
            node_dic = {}
            attrs = n._attributes

            for a in attrs:
                node_dic[a] = attrs[a]
            graph['vertices'] += [node_dic]

        graph['edges'] = []

        for e in doc.graph.edge:
            edge_dic = {}
            attrs = e._attributes

            for a in attrs:
                edge_dic[a] = attrs[a]
            graph['edges'] += [edge_dic]

        return graph

    @staticmethod
    def socs_untangle_to_dict(doc: untangle.Element, agt_type: str):
        socs = []

        for s in doc.society:
            soc_dic = {}
            attrs = s._attributes

            for a in attrs:
                soc_dic[a] = attrs[a]

            soc_dic['agents'] = []

            for agt in s.children:
                attrs = agt._attributes
                agt_dic = {'type': agt_type, "id": attrs["id"], "vertex_id":
                    attrs["node_id"], "allowed_perceptions": []}

                for pcp in agt.allowed_perception:
                    pcp_dic = {}
                    attrs = pcp._attributes

                    for a in attrs:
                        pcp_dic[a] = attrs[a]

                    agt_dic["allowed_perceptions"] += [pcp_dic]

                agt_dic['allowed_actions'] = []

                for act in agt.allowed_action:
                    act_dic = {}
                    attrs = act._attributes

                    for a in attrs:
                        act_dic[a] = attrs[a]

                    agt_dic['allowed_actions'] += [act_dic]

                soc_dic['agents'] += [agt_dic]

            socs += [soc_dic]

        return socs

    @classmethod
    def config_untangle_to_dict(cls, doc: untangle.Element, agt_type: str):
        return {"environment": {"graph": cls.map_untangle_to_dict(
            doc.environment),
            "meta-society": {"id": "_",
                             "societies":
                                 cls.socs_untangle_to_dict(
                                     doc.environment,
                                     agt_type)
                             }
        }
        }

    @classmethod
    def config_xml_to_iterables(cls, path: str):
        return cls.config_dict_to_iterables(cls.config_xml_to_dict(path))

    @classmethod
    def convert_xmls_to_jsons(cls, xmls_path: str, jsons_path: str):
        for root, dirs, files in os.walk(xmls_path):
            for name in files:
                cls.convert_map_xml_to_json(xmls_path + name,
                                            (jsons_path + name).replace(
                                                "xml", "json"))

    @staticmethod
    def load_simple_example():
        branch_number = 6
        vertices_number = branch_number + 1
        edges_number = 2 * branch_number

        graph = np.array([[-1, 0, 1, 2, 3, 4, 5], \
                          [0, -1, 6, -1, -1, -1, 11], \
                          [1, 6, -1, 7, -1, -1, -1], \
                          [2, -1, 7, -1, 8, -1, -1], \
                          [3, -1, -1, 8, -1, 9, -1], \
                          [4, -1, -1, -1, 9, -1, 10], \
                          [5, 11, -1, -1, -1, 10, -1]], dtype=np.int16)

        edge_lgths = np.array([], dtype=np.float16)
        for _ in range(branch_number):
            edge_lgths = np.append(edge_lgths, 4)
        for _ in range(6, edges_number):
            edge_lgths = np.append(edge_lgths, 6)

        return graph, edge_lgths, ["rr", "rr"]
