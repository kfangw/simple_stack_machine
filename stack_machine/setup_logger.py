import logging

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


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