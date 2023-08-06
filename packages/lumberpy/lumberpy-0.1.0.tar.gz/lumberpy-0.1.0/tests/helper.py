import logging
import importlib


def reset_logging_module():
    """The logging module is stateful and therefore must be
       reset before every test
    """
    logging.shutdown()
    importlib.reload(logging)
