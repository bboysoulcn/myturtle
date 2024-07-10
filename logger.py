from loguru import logger
import sys

logger.configure(
    handlers=[{
        "sink": sys.stdout,
        "serialize": False,
        "format": "{time} - {level} - {message} "
    }]
)