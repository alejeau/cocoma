# Test for misc.iterable_same_values

import util.miscellaneous as misc

ar = [[5, 2], [9, 4], [5, 2], [2, 8]]
print(misc.rtrv_sm_v_in_itr(ar))

ar = [[[5, 2], [9, 4], [5, 2], [2, 8]], [[5, 2], [1, 4], [8, 2], [2, 8]],
      [[5, 2], [9, 4], [5, 2], [2, 5]], [[5, 2], [9, 4], [5, 2], [2, 8]]]
print(misc.rtrv_sm_v_in_itr(ar))

