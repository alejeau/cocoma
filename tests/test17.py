# test17: Json config loading

from pprint import pprint

from model.Paths import Paths
from util.SimPreprocessor import SimPreprocessor

config_path = Paths.Configs + "city_traffic/rcd/rr" \
              "-city_traffic-rcd-10-0.json"
graph, fl_edge_lgths, edges_to_vertices, locations, \
            edge_activations, idls, socs, societies_speeds, \
            societies_agts_pos = SimPreprocessor.load_config(config_path)

pprint(socs)