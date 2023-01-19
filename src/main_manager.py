import sys
import os


from init_logger import init_logger
from src.network.manager import Manager

logger_level = int(os.getenv("LOGGER_LEVEL"))
config_file_location = os.getenv("CONFIG_FILE_LOCATION")

init_logger(logger_level)
# logging.getLogger().setLevel(18) # info
#logging.getLogger().setLevel(15) # debug

member = Manager(config_file_location)

# /usr/bin/python3 ./main_manager.py ./resources/config/config_reduced.ini
