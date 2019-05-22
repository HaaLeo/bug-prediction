# ------------------------------------------------------------------------------------------------------
#  Copyright (c) Leo Hanisch. All rights reserved.
#  Licensed under the BSD 3-Clause License. See LICENSE.txt in the project root for license information.
# ------------------------------------------------------------------------------------------------------

from argparse import ArgumentParser
from collections import Counter
from itertools import islice
import logging
from math import exp
import sys
import time

from ._version import __version__
from .scm import SourceControllManager
from .entropy import entropy_for_files

# pylint: disable=undefined-variable

logging.basicConfig(
    format='%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s',
    stream=sys.stdout,
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)


def main():
    args = _get_args()
    if args:
        _run(args)


def _run(args):  # TODO change to **kwargs and move to own file
    decay = args.get('decay')
    period_count = args.get('periods')
    subsystems = args.get('subsystems')
    file_pattern = args['file_pattern']  # TODO use glob
    directory = args['directory']

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
        period_file_entropies = entropy_for_files(change_probability_dist, args['contribution'])

        # Apply exponential decay if option is set
        if decay:
            acc_entropies += exp(decay * (period['end_time']['epoch'] - current_time)) \
                * period_file_entropies
        else:
            acc_entropies += period_file_entropies

    if subsystems:
        pass  # TODO implement subsystem feature
    else:
        result = acc_entropies

    return result


def _get_args():
    parser = ArgumentParser(
        prog='bugprediction',
        description='Predict bugs using the complexity of code changes.')

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='bugprediction v' + __version__,
        help='Show version and exit')
    parser.add_argument(
        '-f',
        '--file-pattern',
        type=str,
        default='.*',
        help='Regex file pattern that indicates which files shall be included (default: .*)'
    )
    parser.add_argument(
        '-d',
        '--directory',
        type=str,
        default='.',
        help='Path to the project root that shall be analyzed')
    parser.add_argument(
        '-c',
        '--contribution',
        type=str,
        default='percentage',
        help='The contribution of a period\'s entropy that will be assigned to a file (default: percentage)',
        choices=['full', 'percentage', 'uniform'])
    parser.add_argument(
        '-d',
        '--decay',
        type=float,
        help='Decay factor for exponential decay of the contribution of earlier file changes. If omitted no decay model will be applied.')
    parser.add_argument(
        '-p',
        '--periods',
        type=int,
        help='Number of periods to be created. If omitted all commits are processed')
    parser.add_argument(
        '-r',
        '--reporter',
        type=str,
        default='pretty',
        help='The report used to report the result',
        choices=['json', 'pretty'])
    parser.add_argument(
        '-s',
        '--subsystems',
        type=str,
        nargs='+',
        help='A relative path to --directory. A subsystems\' entropy is the sum of all entropies of the files it contains.'
    )
    return vars(parser.parse_args())


if __name__ == '__main__':
    main()
