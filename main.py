import logging
import logging.config
import os

from stack_machine.lexer import Lexer

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(__file__)


def setup_logger():
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "simple": {
                    'format': '%(asctime)s [%(process)d] [%(levelname)s] %(message)s',
                }
            },

            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "INFO",
                    "formatter": "simple",
                },

                "info_file_handler": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "INFO",
                    "formatter": "simple",
                    "filename": "{0}/.info.log".format(BASE_DIR),
                    "maxBytes": 10485760,
                    "backupCount": 20,
                    "encoding": "utf8"
                },

                "error_file_handler": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "ERROR",
                    "formatter": "simple",
                    "filename": "{0}/.errors.log".format(BASE_DIR),
                    "maxBytes": 10485760,
                    "backupCount": 20,
                    "encoding": "utf8"
                }
            },

            "loggers": {
                "my_module": {
                    "level": "ERROR",
                    "handlers": ["console"],
                    "propagate": "no"
                }
            },

            "root": {
                "level": "INFO",
                "handlers": ["console", "info_file_handler", "error_file_handler"]
            }
        }
    )


def main():
    setup_logger()
    lexer = Lexer("nop 1 add 2 sub 3 and 4 or xor 5 not push dup 8 drop 10")
    for l in lexer.tokens():
        logger.info(l)


if __name__ == "__main__":
    main()

