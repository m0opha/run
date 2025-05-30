import os

from .print_colors import pSuccess

from ..vars.paths import _CONFIG_FILE_PATH, _CONFIG_PATH
from ..vars.texts import CONFIG_DIRECTORY_CREATED_TEXT, PLEASE_SETTING_UP_CONFIG_FILE_TEXT
from ..vars.content_config_file import content

def verifyConfigDir():
    
    if not os.path.exists(_CONFIG_PATH):
        os.mkdir(_CONFIG_PATH)
        pSuccess(CONFIG_DIRECTORY_CREATED_TEXT)

    if not os.path.exists(_CONFIG_FILE_PATH):
        with open(_CONFIG_FILE_PATH, "w") as file:
            file.writelines(content)
            print(PLEASE_SETTING_UP_CONFIG_FILE_TEXT)
