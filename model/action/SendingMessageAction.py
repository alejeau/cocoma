# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

from model.action.Action import Action
from model.action.Actions import Actions


class SendingMessageAction(Action):
    def __init__(self, _message: str, _agt_id: int):
        Action.__init__(self, "sending_message", Actions.Sending_message)
        self.message = _message
        self.agt_id = _agt_id




