from ..modules.generic_fun import getConfig
from .paths import _CONFIG_FILE_PATH
from .keywords import RUN

_TARGET_FILENAME = RUN
_EXECUTE_ALL_FLAG = False
_CONFIG = getConfig(_CONFIG_FILE_PATH)