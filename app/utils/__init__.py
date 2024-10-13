import logging
import sys
import traceback

import colorlog

from app.constants.string_constants import StringConstants


def setup_logger() -> logging.Logger:
    """
    Sets up and configures the logger. Returns the configured logger.
    """
    logger = logging.getLogger(StringConstants.get_logger_app_name())
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    file_handler = logging.FileHandler("app_errors.log")
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )

    custom_colors: dict = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    }

    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            log_colors=custom_colors,
        )
    )

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


app_logger = setup_logger()


def log_exception() -> None:
    """
    Logs the current exception with detailed traceback using the configured logger.
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    tb_text = "".join(tb_lines)
    app_logger.error("Exception occurred:\n%s", tb_text)
