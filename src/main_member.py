import sys
import os

from init_logger import init_logger
from src.network.member import Member


# logging.getLogger().setLevel(18) # info
# logging.getLogger().setLevel(15) # debug

id_of_member = os.getenv("ID_OF_MEMBER")
config_file_location = os.getenv("CONFIG_FILE_LOCATION")
logger_level = int(os.getenv("LOGGER_LEVEL"))

init_logger(logger_level)
member = Member(config_file_location , id_of_member)

# /usr/bin/python3 ./main_member.py ./resources/config/config_reduced.ini 1
