# test9.py: test about conversion from a sim dict to iterables
from util.miscellaneous import *
from pprint import pprint

xml_path = Paths.Sim_materials + "cr-islands-soc_0_10-0.xml"
json_path = Paths.Sim_materials + "cr-islands-soc_0_10-0.json"
d = config_xml_to_dict(xml_path)
#pprint(d)
#pprint(d['environment']['societies'])

# graph, fl_edge_lgths = sim_dict_to_np_arrays(d)
graph, fl_edge_lgths, socs, edges_to_vertices, locations, edge_activations, \
idls, speeds, agts_pos = sim_xml_to_iterables(xml_path)

xml_to_json(xml_path, json_path)

pprint(agts_pos)
pprint(socs)
pprint(speeds)
pprint(graph)
pprint(fl_edge_lgths)
