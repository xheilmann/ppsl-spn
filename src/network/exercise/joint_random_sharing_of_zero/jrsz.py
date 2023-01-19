from src.network.exercise.exercise_class import Exercise
from src.globals import IDs


def add_exercise_jrsz(manager, data_id_result):
    manager.exercises.append(Exercise(IDs.JRSZ_SHARING_STEP, data_id_result))
    manager.exercises.append(Exercise(IDs.JRSZ_RESULT_STEP, data_id_result))


def jrsz_sharing_step(member, message_value):
    data_id_result = message_value
    member.insert_in_share_additive(data_id_result, member.prim_number)
    member.network_socket.send(member.manager_id_chip, IDs.JRSZ_SHARING_STEP, member.id)


def jrsz_result_step(member, message_value):
    data_id_result = message_value
    member.join_additive_shares(data_id_result)
    member.network_socket.send(member.manager_id_chip, IDs.JRSZ_RESULT_STEP, member.id)
