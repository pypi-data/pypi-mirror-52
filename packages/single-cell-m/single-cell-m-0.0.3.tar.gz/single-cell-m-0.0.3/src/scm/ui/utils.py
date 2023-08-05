import logging
import json
import sys
import os.path
from datetime import datetime

from mgkit.workflow.utils import PrintManAction
from .. import VERSION


def basic_ui_options(parser, manual=''):

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-v',
        '--verbose',
        action='store_const',
        const=logging.DEBUG,
        default=logging.INFO,
        help='more verbose - includes debug messages',
        dest='verbose'
    )
    group.add_argument(
        '--quiet',
        action='store_const',
        const=logging.ERROR,
        help='less verbose - only error and critical messages',
        dest='verbose'
    )

    parser.add_argument(
        '--manual',
        action=PrintManAction,
        manual=manual
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {0}'.format(VERSION)
    )

def write_manifest(output_dir):

    json.dump(
        dict(
            script=os.path.basename(sys.argv[0]),
            command=sys.argv[1],
            version=VERSION,
            cmd_line=' '.join(sys.argv),
            datetime=str(datetime.now())
        ),
        open(
            os.path.join(
                output_dir,
                '{}-manifest.json'.format(sys.argv[1])
            ),
            'w'
        ),
    )
