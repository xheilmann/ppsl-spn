from init_logger import init_logger
from src.network.member import Member
from src.network.manager import Manager

config_file_path = "../resources/config/config_tretail_5_server.ini"

init_logger(18)


# from structure import replace_sum_node_weights

# replace_sum_node_weights(member.spn)
# print(member.spn_to_str_equation())

manager_0 = Manager(config_file_path)

member_1 = Member(config_file_path, "1")
member_4 = Member(config_file_path, "4")
member_2 = Member(config_file_path, "2")
member_5 = Member(config_file_path, "5")
member_3 = Member(config_file_path, "3")


# at websockets.legacy.framing in Class Frame the measurement is induced
