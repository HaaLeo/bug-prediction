# ------------------------------------------------------------------------------------------------------
#  Copyright (c) Leo Hanisch. All rights reserved.
#  Licensed under the BSD 3-Clause License. See LICENSE.txt in the project root for license information.
# ------------------------------------------------------------------------------------------------------

import logging
import sys
import argparse
from ._version import __version__

# pylint: disable=undefined-variable

logging.basicConfig(
    format='%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s',
    stream=sys.stdout,
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        prog='bugprediction',
        description='Predict bugs using the complexity of code changes.')

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='bugprediction v' + __version__,
        help='Show version and exit')

    args = vars(parser.parse_args())
    if args:
        print('hello world')
    else:
        parser.print_usage()


if __name__ == '__main__':
    main()
