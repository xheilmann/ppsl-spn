from src.network.exercise.exercise_class import Exercise
from src.globals import IDs


def add_exercise_jrpz(manager, data_id_result):
    manager.exercises.append(Exercise(IDs.JRPZ_SHARING_STEP, data_id_result))
    manager.exercises.append(Exercise(IDs.JRPZ_RESULT_STEP, data_id_result))


def jrpz_sharing_step(member, message_value):
    data_id_result = message_value
    member.insert_in_share(data_id_result, 0)
    member.network_socket.send(member.manager_id_chip, IDs.JRPZ_SHARING_STEP, member.id)


def jrpz_result_step(member, message_value):
    data_id_result = message_value
    member.join_polynomial_shares(data_id_result)
    member.network_socket.send(member.manager_id_chip, IDs.JRPZ_RESULT_STEP, member.id)
