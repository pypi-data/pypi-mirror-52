import os

import yaml


DEFAULT_LOG_FORMAT = "{asctime} {levelname:3.3} {name}: {message}"


def get(config_path: str = None) -> dict:
    if config_path is None:
        config_path = os.environ.get("LUMBER_CONFIG_PATH", None)

    if not config_path:
        return {}

    with open(config_path) as f:
        config = yaml.safe_load(f)

    if not isinstance(config, dict):
        raise ValueError("An invalid config was supplied, must be dict/object")

    return config


def ensure_defaults(config: dict) -> None:
    config.setdefault("version", 1)

    # Prevents loggers created before configuration to be disabled
    # All active handlers will be removed though
    config.setdefault("disable_existing_loggers", False)

    # always need a default formatter, handler and logger
    config.setdefault("formatters", {})
    config.setdefault("handlers", {})
    config.setdefault("loggers", {})

    default_log_format = os.environ.get("LUMBER_FORMAT", DEFAULT_LOG_FORMAT)
    default_log_format = config.pop("default_log_format", default_log_format)
    default_log_level = os.environ.get("LUMBER_LEVEL", "INFO")
    default_log_level = config.pop("default_log_level", default_log_level)

    default_formatter = {
        "format": default_log_format,
        "class": "lumberpy.colored_formatter.ColoredFormatter",
        "style": "{",
    }

    default_handler = {
        "level": default_log_level,
        "class": "logging.StreamHandler",
        "formatter": "default",
        "stream": "ext://sys.stdout",
    }

    # logging to console can be disabled by setting the console handler to None
    config["handlers"].setdefault("console", default_handler)

    default_handlers = [
        handler
        for handler in config["handlers"].keys()
        if config["handlers"][handler] is not None
    ]

    default_logger = {"level": default_log_level, "handlers": default_handlers}

    config["formatters"].setdefault("default", default_formatter)

    # set the global root logger config
    registered_loggers = config["loggers"].keys()
    if "" not in registered_loggers:
        config["loggers"].setdefault("", default_logger)

    config.setdefault("show_warnings", True)


def validate_config(config: dict) -> None:
    # TODO
    pass
