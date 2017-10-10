# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

import numpy as np

from model.perception.Perception import Perception


class GraphPerception(Perception):

    def __init__(self, graph_arg, edge_activations_arg):
        """
        :param graph_arg : graph perceived for the case where it is dynamic
        :type graph_arg : list
        """
        Perception.__init__(self, "graph", 2)

        self.graph = np.array(graph_arg, np.int16)
        self.edge_activations = np.array(edge_activations_arg, np.int16)





