import logging

from core.utils.env import getenv


def setup_logging():
    root_logger = logging.getLogger()
    stream_handler = logging.StreamHandler()
    # Version is either a git commit hash or a git tag
    # or "local" when executed
    version = getenv("IMAGE_TAG", "local")
    # We are using Loki as log collector thus we don't use a structured logging
    formatter = logging.Formatter(
        f"[%(asctime)s] [{version}] [%(levelname)s]: %(message)s"
    )
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

    log_level = getenv("LOG_LEVEL", "INFO")
    log_level_value = getattr(logging, log_level.upper(), None)
    root_logger.setLevel(log_level_value)
