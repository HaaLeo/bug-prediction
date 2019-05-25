# ------------------------------------------------------------------------------------------------------
#  Copyright (c) Leo Hanisch. All rights reserved.
#  Licensed under the BSD 3-Clause License. See LICENSE.txt in the project root for license information.
# ------------------------------------------------------------------------------------------------------

import sys
from argparse import ArgumentParser
import logging

from ._version import __version__
from .predict import predict

# pylint: disable=undefined-variable

logging.basicConfig(
    format='%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s',
    stream=sys.stdout,
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)


def main():
    args = _get_args()
    if args:
        predict(**args)


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
        '-D',
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
