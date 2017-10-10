import json
from pprint import pprint

from util.SimPreprocessor import SimPreprocessor

op = SimPreprocessor.generate_blank_config(1, [10], [["rr"] * 10],
                                           sn=["rcd"])
print(op)

with open(op, 'r') as s:
    pprint(json.load(s))

