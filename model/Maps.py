# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

from model.Paths import Paths


class Maps:
    City_Traffic = 0

    Islands = 1

    A = 2

    B = 3

    Circle = 4

    Corridor = 5

    Grid = 6

    id_to_name = ["city_traffic", "islands", "map_a", "map_b", "map_circle",
                  "map_corridor", "map_grid"]

    id_to_path = [Paths.Json_maps + n + ".json" for n in id_to_name]



