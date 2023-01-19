from init_logger import init_logger
from src.network.member import Member
from src.network.manager import Manager

config_file_path = "../resources/config/config_nltcs_10_server.ini"

init_logger(18)


# from structure import replace_sum_node_weights

# replace_sum_node_weights(member.spn)
# print(member.spn_to_str_equation())

manager_0 = Manager(config_file_path)

member_1 = Member(config_file_path, "1")
member_4 = Member(config_file_path, "4")
member_2 = Member(config_file_path, "2")
member_5 = Member(config_file_path, "5")
member_8 = Member(config_file_path, "8")
member_9 = Member(config_file_path, "9")
member_6 = Member(config_file_path, "6")
member_3 = Member(config_file_path, "3")
member_7 = Member(config_file_path, "7")
member_10 = Member(config_file_path, "10")

# at websockets.legacy.framing in Class Frame the measurement is induced
