# This file extracts the average idleness from the logs

import json
# import pprint

from model.Paths import Paths

log_path = Paths.Logs + "islands/hi/10/hi-islands-soc_0-10-0.log.json"

logs = None
# pp = pprint.PrettyPrinter()  # human-readable printing


def load_logs(path):
    with open(path) as file:
        return json.load(file)


def print_avg_idls():
    logs = load_logs(log_path)
    print("Average idleness: " + str(logs[0]))
    # pp.pprint(l)

print_avg_idls()