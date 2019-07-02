# ------------------------------------------------------------------------------------------------------
#  Copyright (c) Leo Hanisch. All rights reserved.
#  Licensed under the BSD 3-Clause License. See LICENSE.txt in the project root for license information.
# ------------------------------------------------------------------------------------------------------

#pylint: disable=too-many-locals
"""
This module represents the history complexity metric.
"""

from collections import Counter, OrderedDict
from math import log, exp
from os import path
from itertools import islice
import time
from .scm import SourceControllManager


def calculate_hcm(**kwargs):
    decay = kwargs.get('decay')
    period_count = kwargs.get('periods')
    subsystems = kwargs.get('subsystems')
    directory = path.normpath(kwargs['directory'])
    file_glob = path.join(directory, kwargs['file_glob'])

    # Accumulated entropies
    acc_entropies = Counter()
    manager = SourceControllManager(directory)
    current_time = time.time()

    # Trim the iterator to the specified amount of periods
    periods_iterator = islice(manager.iter_change_periods(file_glob), period_count)

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
            # Apply decay on all files
            for file_name in period_file_entropies:
                period_file_entropies[file_name] *= \
                    exp(decay * (period['end_time']['epoch'] - current_time))

        acc_entropies += period_file_entropies

    if subsystems:
        subsystem_entropies = Counter()
        for subsystem in subsystems:
            for file_name in acc_entropies:
                if file_name.startswith(subsystem.strip('./')):
                    subsystem_entropies[subsystem] += acc_entropies[file_name]
    else:
        subsystem_entropies = acc_entropies

    # Order result
    result = OrderedDict(subsystem_entropies.most_common())
    return result, manager.lastest_commit


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
