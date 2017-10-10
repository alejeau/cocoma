# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

import numpy as np

from model.action.Actions import Actions
from model.action.Action import Action


class MovingToAction(Action):
    def __init__(self, __from: tuple, __to: tuple):
        """
        :param _from_arg: iterable
        :type _from_arg:
        :param _to_arg: iterable
        :type _to_arg:
        """
        Action.__init__(self, 'moving_to', Actions.Moving_to)
        self._from = __from
        self._to = __to