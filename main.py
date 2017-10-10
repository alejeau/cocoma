# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

# import json
# import pprint

from control.Ananke import Ananke
from control.Archivist import Archivist
from model.Paths import Paths
from util.net.SimulatedConnection import SimulatedConnection

# config_path = "various/sim_materials/configs/cr--soc_0_10-0.json"
# log_path = "various/sim_materials/configs/cr--soc_0_10-0.log.json"

config_path = Paths.Configs + "islands/rcted/10/rcted-islands-soc_0-10-0.json"
log_path = Paths.Logs + "islands/rcted/10/rcted-islands-soc_0-10-0.log.json"


cycle_number = 3000 # was 3000
depth = 3

ar_cnn = SimulatedConnection()
archivist = Archivist(ar_cnn, log_path, cycle_number)
# archivist.start()

# Display
# d_cnn = SimulatedConnection()
# display_addr = None
# display_addr.start()

# Ananke connection
an_cnn = SimulatedConnection()

ananke = Ananke(an_cnn, config_path, archivist, cycle_number, depth)
ananke.start()

