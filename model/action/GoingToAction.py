# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

import numpy as np

from model.action.Actions import Actions
from model.action.Action import Action


class GoingToAction(Action):
    def __init__(self, _goal_position: object) -> object:
        """
        :param _goal_node: iterable
        :type _goal_node:
        """
        Action.__init__(self, 'going_to', Actions.Going_to)
        self.goal_position = _goal_position
