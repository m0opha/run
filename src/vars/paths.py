import os

from .keywords import *

_APP_NAME = RUN
_TARGET_FILENAME = RUN
_CURRENT_DIR = os.getenv(PWD)

_CONFIG_PATH = os.path.join(
    os.getenv(HOME), 
    CONFIG, 
    _APP_NAME
    )

_CONFIG_FILE_PATH = os.path.join(
    _CONFIG_PATH, 
    "config.txt"
    )
