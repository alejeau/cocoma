# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

import numpy as np

import util.miscellaneous as misc

from model.perception.Perception import Perception


class SelfPerception(Perception):

    def __init__(self, position : np.ndarray):
        Perception.__init__(self, "self", 0)
        self.pos = position

    def to_string(self, indent_1 : int, indent_2 : int):
        indent_str_1 = misc.indent(indent_1)
        indent_str_2 = misc.indent(indent_2)
        print(indent_str_1 + "SelfPerception:\n",
              indent_str_2 + "Type: ", self.type, "\n",
              indent_str_2 + "Name: ", self.name, "\n",
              indent_str_2 + "Position: ", self.pos, "\n")