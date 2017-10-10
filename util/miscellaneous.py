# Copyright (C) ONERA, Inc, Laboratoire LIP6 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Mehdi Othmani-Guibourg <mehdi.othmani@lip6.fr>, September, 2017

from model.Maps import Maps
from model.Paths import Paths
from util.spaceprocessor import *


def _min(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    c = a <= b
    return a * c + (1 - c) * b


def indent(width: int):
    r = ""
    for i in range(width):
        r += " "
    return r


def name_config_file(m: int, agts_nbs: list, sats: list = None, sn: str = '',
                     pfx: str = '', sfx: str = '', dp: str = '') -> str:
    """
    :param m:
    :type m:
    :param agts_nbs:
    :type agts_nbs:
    :param sats:
    :type sats:
    :param sn:
    :type sn:
    :param e: execution number.
    :type e:
    :param sfx: suffix
    :param pfx:
    :type sfx: str
    :param dp:
    :type dp:
    :return:
    :rtype:
    """

    if pfx == '':
        # If sats is not empty
        if len(sats) > 0:
            # If the agents in the first society share the same strategy
            if len(sats[0]) == 1:
                pfx = sats[0][0]
            # Else if this is a coordinated strategy where except the
            # coordinator, all others agents share the same strategy
            else:
                c_str = True
                for i in range(2, len(sats[0])):
                    if sats[0][i] != sats[0][i - 1]:
                        c_str = False
                        break
                if c_str:
                    pfx = sats[0][1]
            # TODO: Handle the case where there are others societies

    if sn == '':
        sn = name_society(agts_nbs)

    if dp == '':
        dp = Paths.Configs + \
             Maps.id_to_name[m] + "/" + \
             sn + "/" + \
             sum(agts_nbs) + "/"

    return dp + \
           pfx + \
           ('-' if pfx != '' else '') + Maps.id_to_name[m] + \
           '-' + sn + \
           ('-' if len(agts_nbs) > 0 else '') + \
           '-'.join(str(n) for n in agts_nbs) + \
           '-' + sfx + \
           ".json"


def name_society(agts_nbs: list = None, sfx: str = ''):
    return ("metasoc_" if len(agts_nbs) > 1 else "" if len(agts_nbs) == 0
    else "soc_") + sfx


# Retrieve the identical values in an iterable
def rtrv_sm_v_in_itr(itr):
    """
    :param itr:
    :type itr: iterable
    :return:
    :rtype:
    """

    # The output
    o = []

    # Already added ids
    aai = []

    for i in range(len(itr)):
        if i not in aai:
            aai += [i]
            # Temporary output: the itr's ids having the same current value
            to = []
            for j in range(len(itr)):
                if itr[i] == itr[j]:
                    to += [j]
                    aai += [j]

            o += [to]

    return o
