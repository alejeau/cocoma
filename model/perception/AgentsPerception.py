# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

import numpy as np

from model.perception.Perception import Perception
import util.miscellaneous as misc


class AgentsPerception(Perception):

    def __init__(self, agts_pos_arg: np.ndarray):
        """
        :param agts_pos_arg:
        :type agts_pos_arg: numpy.ndarray
        """
        Perception.__init__(self, "agents", 1)

        self.agts_pos = agts_pos_arg

    def to_string(self, indent_1 : int, indent_2 : int):
        indent_str_1 = misc.indent(indent_1)
        indent_str_2 = misc.indent(indent_2)
        print(indent_str_1 + "AgentsPerception:\n",
              indent_str_2 + "Position: ", self.agts_pos, "\n")

