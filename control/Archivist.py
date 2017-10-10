# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

import numpy as np
import json
import os
import pickle

from control.Artifact import Artifact
from model.Data import Data
from util.net.Connection import Connection


class Archivist(Artifact):
    def __init__(self, _cnn: Connection, _log_path: str, _cycles_nb: int):
        Artifact.__init__(self, _cnn)

        self.cycles_nb = _cycles_nb
        self.log_path = _log_path
        self.log_list = [None] * self.cycles_nb

        # Transient evaluation criteria
        self.tec = []

    def run(self):
        print("Archivist: starting.")

        t = 0

        while not self.stop_working:
            while t < self.cycles_nb:
                self.receive()
                while len(self.messages) != 0:
                    m = self.messages.popleft()
                    data = pickle.loads(m)

                    self.log(data[Data.Cycle], data[Data.Agts_pos],
                             data[Data.Idls])
                t += 1

            self.save_log()
            self.stop_working = True

        print("Archivist stops to work.")

    def log(self, cycle: int, agts_pos: list, idls: list):
        self.log_list[cycle] = [agts_pos, idls]
        self.tec += [np.mean(idls)]

    def save_log(self):
        self.log_list = [[np.mean(self.tec)], self.log_list]
        directory = os.path.dirname(self.log_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(self.log_path, 'w') as s:
            json.dump(self.log_list, s)
