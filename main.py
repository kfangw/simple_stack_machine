import logging.config

from stack_machine.parser import Parser
from stack_machine.setup_logger import setup_logger

logger = logging.getLogger(__name__)


def main():
    setup_logger()

    parser = Parser()
    top = parser.parse_toplevel("nop 1 add 2 sub 3 and 4 or xor 5 not push dup 8 drop 10")
    logger.info(top.dump())


if __name__ == "__main__":
    main()

