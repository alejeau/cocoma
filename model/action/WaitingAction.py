# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

from model.action.Action import Action
from model.action.Actions import Actions


class WaitingAction(Action):
    def __init__(self, _pos: tuple):
        Action.__init__(self, "waiting", Actions.Waiting)
        self.pos = _pos




