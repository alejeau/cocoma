# test16: Test for SimProcessor.generate_configs

from util.SimPreprocessor import SimPreprocessor


ms = [0, 1]

'''
mats = [[["rr"] * 10, ["rr"] * 2], [["cr"] * 10, ["cr"] * 2]]
agts_nbss = [[10, 2], [10, 2]]
cdtrss = [[False, False], [False, False]]
SimPreprocessor.generate_configs(ms, agts_nbss, mats, cdtrss)

mats = [[["rr"]]]
cdtrss = [[False]]
agts_nbss = [[10]]
SimPreprocessor.generate_configs(ms, agts_nbss, mats, cdtrss)


mats = [[["rcd"] * 10]]
mats[0][0][0] = "rcr"
agts_nbss = [[10]]
cdtrss = [[True]]
SimPreprocessor.generate_configs(ms, agts_nbss, mats, cdtrss)
'''

mats = [[["rr"] * 5], [["rr"] * 10], [["rr"] * 15], [["rr"] * 25],
        [["rcr"] + ["rcd"] * 4], [["rcr"] + ["rcd"] * 9], [["rcr"] + ["rcd"]
        * 14], [["rcr"] + ["rcd"] * 24]]

agts_nbss = [[5], [10], [15], [25], [5], [10], [15], [25]]
cdtrss = [[False], [False], [False], [False], [True], [True], [True],
          [True], [True]]
sns = []
SimPreprocessor.generate_configs(ms, agts_nbss, mats, cdtrss)