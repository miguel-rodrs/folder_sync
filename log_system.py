import logging
from logging.handlers import RotatingFileHandler

MAX_SIZE = 100000
MAX_FILES = 3
FORMAT = "%(asctime)s %(message)s"


class CustomFormatter(logging.Formatter):
    """CustomFormatter used to change the color of the different logging levels."""

    def __init__(self, is_file=False):
        grey = "\x1b[34;20m"
        yellow = "\x1b[33;20m"
        red = "\x1b[31;20m"
        bold_red = "\x1b[31;1m"
        blue = "\x1b[36;1m"
        reset = "\x1b[0m"
        format = FORMAT
        self.FORMATS = {
            logging.DEBUG: (grey if not is_file else "") + format + (reset if not is_file else ""),
            logging.INFO: (blue if not is_file else "") + format + (reset if not is_file else ""),
            logging.WARNING: (yellow if not is_file else "") + format + (reset if not is_file else ""),
            logging.ERROR: (red if not is_file else "") + format + (reset if not is_file else ""),
            logging.CRITICAL: (bold_red if not is_file else "") + format + (reset if not is_file else "")
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def create_log(filepath, level=logging.DEBUG):
    """Creates the logging system with the format used in 'CustomFormatter' class."""
    logger = logging.getLogger()
    logger.setLevel(level)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(CustomFormatter())
    logger.addHandler(stream_handler)

    file_handler = RotatingFileHandler(filename=filepath, maxBytes=MAX_SIZE, backupCount=MAX_FILES)
    file_handler.setFormatter(CustomFormatter(is_file=True))
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

