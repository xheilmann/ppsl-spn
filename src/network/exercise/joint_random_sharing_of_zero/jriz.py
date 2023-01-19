from src.network.exercise.exercise_class import Exercise
from src.globals import IDs


def add_exercise_jriz(manager, data_id_result):
    manager.exercises.append(Exercise(IDs.JRIZ_SHARING_STEP, data_id_result))
    manager.exercises.append(Exercise(IDs.JRIZ_RESULT_STEP, data_id_result))


def jriz_sharing_step(member, message_value):
    data_id_result = message_value
    member.insert_in_share_additive_integer(data_id_result, 0)
    member.network_socket.send(member.manager_id_chip, IDs.JRIZ_SHARING_STEP, member.id)


def jriz_result_step(member, message_value):
    data_id_result = message_value
    member.join_additive_integer_shares(data_id_result)
    member.network_socket.send(member.manager_id_chip, IDs.JRIZ_RESULT_STEP, member.id)
