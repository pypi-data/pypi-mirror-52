__author__ = """Fabian Elsner"""
__email__ = "f.elsner@greyrook.com"
__version__ = "0.1.0"

import logging.config

import lumberpy.config
import lumberpy.colored_formatter  # always import it to ensure logging.dictConfig finds it

LOG = logging.getLogger(__name__)


def setup(config_path: str = None, verbose: int = 0) -> None:
    config = lumberpy.config.get(config_path)

    if verbose:
        # at verbose = 1 we want logging.DEBUG
        # at 2 we want one below logging.DEBUG
        default_log_level = logging.DEBUG
        default_log_level -= verbose - 1
        if default_log_level <= 0:
            # log level = 0 means "not set"
            LOG.warning("verbosity level over maximum")
            default_log_level = 1

        config["default_log_level"] = default_log_level

    lumberpy.config.ensure_defaults(config)
    # TODO: validate_config(config)
    logging.config.dictConfig(config)
