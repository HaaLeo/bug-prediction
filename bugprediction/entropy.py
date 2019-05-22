# ------------------------------------------------------------------------------------------------------
#  Copyright (c) Leo Hanisch. All rights reserved.
#  Licensed under the BSD 3-Clause License. See LICENSE.txt in the project root for license information.
# ------------------------------------------------------------------------------------------------------

#pylint: disable=useless-object-inheritance

from collections import Counter
from math import log

def entropy_for_files(file_change_dist, contribution_arg):
    ent = 0.
    base = len(file_change_dist)
    if base == 1:
        # Edge case: dist contains only one value with probability 1.0
        ent = 0
    else:
        for value in file_change_dist.values():
            ent -= value * log(value, base)

    # Weight the entropy with the contribution factor
    entropies = [c * ent for c in _get_contribution_factors(file_change_dist, contribution_arg)]

    # Build dict of entropies
    result = {key: value for key, value in zip(file_change_dist.keys(), entropies)}
    return Counter(result)

def _get_contribution_factors(dist, contribution_arg):
    if contribution_arg == 'full':
        contribution = [1] * len(dist)
    elif contribution_arg == 'percentage':
        contribution = dist.values()
    elif contribution_arg == 'uniform':
        contribution = [1/len(dist)] * len(dist)
    else:
        raise ValueError('"%s" is an invalid argument.' % contribution_arg)

    return contribution
