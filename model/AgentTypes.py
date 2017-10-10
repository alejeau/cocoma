# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

from control.agent.RandomCoordinated import RandomCoordinated
from control.agent.RandomCoordinator import RandomCoordinator
from control.agent.RandomReactive import RandomReactive
from control.agent.HighestIdleness import HighestIdleness
from control.agent.RandCoordinated import RandCoordinated
from control.agent.RandCoordinator import RandCoordinator


class AgentTypes:
    NoType = -1

    # Random Reactive
    RR = 0

    # Conscientious Reactive
    CR = 1

    # Random Coordinated
    RCd = 2

    # Random Coordinator
    RCr = 3

    # HighestIdleness
    HI = 4

    # RandCoordinated
    RndCted = 5

    # RandCoordinator
    RndCtor = 6

    # Heuristic Pathfinder Cognitive Coordinated
    # HPCC = 7

    str_to_id = {"rr": RR,
                 "cr": CR,
                 "rcd": RCd,
                 "rcr": RCr,
                 "hi" : HI,
                 "rcted" : RndCted,
                 "rctor" : RndCtor
                 # "hpcc": HPCC
                 }

    id_to_class_name = [RandomReactive, RandomReactive, RandomCoordinated,
                        RandomCoordinator,
                        HighestIdleness,
                        RandCoordinated, RandCoordinator
                        # , HPCC
                        ]
