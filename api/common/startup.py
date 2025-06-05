import sys
from os import path
from loguru import logger

def get_file_logger_config(log_directory: str) -> dict:
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

def get_stdout_logger_config() -> dict:
    stdout_logger_config = {
        "handlers": [
            {
                "sink": sys.stdout,
                "level": "ERROR",
                "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
            },
        ]
    }
    return stdout_logger_config
