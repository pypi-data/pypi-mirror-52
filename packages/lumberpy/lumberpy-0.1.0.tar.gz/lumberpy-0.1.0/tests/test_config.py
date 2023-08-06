import lumberpy.config

from . import helper


def setup_function():
    helper.reset_logging_module()


def test_ensure_defaults():
    config = {}
    lumberpy.config.ensure_defaults(config)

    assert config["disable_existing_loggers"] is False
    assert "default" in config["formatters"]
    assert "console" in config["handlers"]
    assert "" in config["loggers"]

    # existing values must not be overwritten
    formatter = {}
    config = {"disable_existing_loggers": True, "formatters": {"default": formatter}}

    lumberpy.config.ensure_defaults(config)

    assert config["disable_existing_loggers"] is True
    assert config["formatters"]["default"] is formatter
