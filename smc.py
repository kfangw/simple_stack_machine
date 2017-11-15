import logging.config

import os

from stack_machine.driver import Driver
from stack_machine.setup_logger import setup_logger

from optparse import OptionParser
from optparse_mooi import CompactColorHelpFormatter

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(__file__)


def main():
    parser = OptionParser(
        formatter=CompactColorHelpFormatter(),
        usage="usage: python ./%prog [options] filename",
        version="%prog 0.1"
    )
    parser.add_option(
        "-o", "--output",
        action="store",
        dest="output_file",
        default=None,
        help="File name for executable code",
    )
    parser.add_option(
        "-k", "--keep-ir",
        action="store_true",
        dest="keep",
        default=False,
        help="Keep intermediate files"
    )
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("wrong option. Check --help option")

    input_file_name = args[0]
    output_file_name = options.output_file
    if not output_file_name:
        output_file_name = input_file_name.split('.')[0] + ".out"

    setup_logger(BASE_DIR)
    driver = Driver(BASE_DIR, input_file_name, output_file_name, options.keep)
    driver.compile()


if __name__ == "__main__":
    main()
