import sys
from os import path
from . import get_bool_env
from loguru import logger
from typing import List

def _get_file_logger_config(log_directory: str) -> dict:
    logger_config = {
        "handlers": [
            {
                "sink": path.join(log_directory, "debug.log"),
                "level": "DEBUG",
                "filter": lambda record: record["level"].no <= logger.level("WARNING").no,
                "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
                "rotation": "10 MB",
                "retention": "30 days",
                "compression": "zip",
            },
            {
                "sink": path.join(log_directory, "error.log"),
                "level": "ERROR",
                "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
                "rotation": "10 MB",
                "retention": "30 days",
                "compression": "zip",
                "backtrace": True,
                "diagnose": True,
            },
        ]
    }
    return logger_config

def _get_stdout_logger_config() -> dict:
    stdout_logger_config = {
        "handlers": [
            {
                "sink": sys.stdout,
                "level": "DEBUG",
                "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
            },
        ]
    }
    return stdout_logger_config

def get_logger_config(command_line_args: List[str], logs_directory: str):

    IS_TEST_OR_CI = 'test' in command_line_args or get_bool_env(env_var_name="CI")

    if IS_TEST_OR_CI:
        return _get_stdout_logger_config()
    return _get_file_logger_config(logs_directory)
