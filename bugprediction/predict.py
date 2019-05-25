# ------------------------------------------------------------------------------------------------------
#  Copyright (c) Leo Hanisch. All rights reserved.
#  Licensed under the BSD 3-Clause License. See LICENSE.txt in the project root for license information.
# ------------------------------------------------------------------------------------------------------

#pylint: disable=useless-object-inheritance

from os import path
from collections import Counter
from math import log, exp
from itertools import islice
import time
from .scm import SourceControllManager

def predict(**kwargs):
    decay = kwargs.get('decay')
    period_count = kwargs.get('periods')
    subsystems = kwargs.get('subsystems')
    directory = kwargs['directory']
    file_pattern = kwargs['file_pattern']

    # Accumulated entropies
    acc_entropies = Counter()
    manager = SourceControllManager(directory)
    current_time = time.time()

    # Trim the iterator to the specified amount of periods
    periods_iterator = islice(manager.iter_change_periods(file_pattern), period_count)

    for period in periods_iterator:
        overall_changes = sum(period['changes'].values())
        change_probability_dist = {
            file_name: period['changes'][file_name]/overall_changes
            for file_name in period['changes']
        }

        # The entropy for all files of the current period
        period_file_entropies = _entropy_for_files(change_probability_dist, kwargs['contribution'])

        # Apply exponential decay if option is set
        if decay:
            acc_entropies += exp(decay * (period['end_time']['epoch'] - current_time)) \
                * period_file_entropies
        else:
            acc_entropies += period_file_entropies

    if subsystems:
        result = Counter()
        for subsystem in subsystems:
            for file_name in acc_entropies:
                if file_name.startswith(subsystem.strip('./')):
                    result[subsystem] += acc_entropies[file_name]
    else:
        result = acc_entropies

    return result


def _entropy_for_files(file_change_dist, contribution_arg):
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
