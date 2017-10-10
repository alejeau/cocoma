# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

from threading import Thread
from collections import deque

import util.miscellaneous as misc
from util.net.Connection import Connection


class Artifact(Thread):
    def __init__(self, _cnn: Connection):
        Thread.__init__(self)

        # Network and messages
        self.cnn = _cnn

        self.messages = deque()

        # Various
        self.ac = False  # artifact cycle completed

        self.stop_working = False

    #  Messages
    def send(self, message, address):
        self.cnn.send(message, address)

    def receive(self):
        # self.cnn.receive()
        buffer = self.cnn.get_buffer_and_flush()
        for m in buffer:
            self.messages.append(m)

    def __str__(self):
        # TODO Fulfill with missing attributes

        indent_str_1 = misc.indent(0)
        indent_str_2 = misc.indent(2)

        s = indent_str_1 + self.__class__.__name__ + ":\n" \
            + indent_str_2 + "Action completed : " + str(self.ac) + "\n\n" \
            + indent_str_2 + "Stop working : " + str(self.stop_working) + \
            "\n\n"

        return s
