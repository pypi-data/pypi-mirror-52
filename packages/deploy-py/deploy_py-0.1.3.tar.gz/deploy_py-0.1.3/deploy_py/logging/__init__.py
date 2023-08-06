import logging
import sys


_logger = None


def get_logger(name: str = "deploy.logger", level: int = 0):
    global _logger

    if _logger is None:
        _logger = logging.getLogger(name)
    log_formatter = logging.Formatter('%(message)s')

    if len(_logger.handlers) == 0:
        ch = logging.StreamHandler(sys.stderr)
        ch.setFormatter(log_formatter)
        _logger.addHandler(ch)

    log_level = {
        0: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG,
    }.get(level, logging.DEBUG)

    _logger.setLevel(log_level)
    return _logger

