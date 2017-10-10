# test8.py: test about conversion from a sim xml to a sim json
from pprint import pprint

from model.Paths import Paths
from util.SimPreprocessor import SimPreprocessor

data = SimPreprocessor.config_xml_to_dict(
    Paths.Configs + 'cr-islands-soc_0_10-0.xml')
pprint(data)

SimPreprocessor.convert_config_xml_to_json(Paths.Configs +
                                           'cr-islands-soc_0_10-0.xml',
                                           Paths.Configs +
                                           'cr-islands-soc_0_10-0.json')

xml = '<?xml version="1.0"?>' \
      '<root>' \
      '<child name="child1">' \
        '<sibling name="sibling1"/>' \
      '</child>' \
      '<child name="child2">' \
        '<sibling name="sibling2"/>' \
      '</child>' \
      '</root>'



