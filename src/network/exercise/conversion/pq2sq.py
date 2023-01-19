from src.network.exercise.exercise_class import Exercise
from src.globals import IDs

from src.network.member import Member


def add_exercise_pq2sq(manager, data_id, data_id_result=None):
    if data_id_result is None:
        data_id_result = data_id
    manager.exercises.append(Exercise(IDs.PQ2SQ_RESHARING_STEP, data_id))
    manager.exercises.append(
        Exercise(IDs.PQ2SQ_RESULT_STEP, f"{data_id};{data_id_result}")
    )


def pq2sq_resharing_step(member, message_value):
    data_id = message_value
    member.insert_in_share_additive(data_id, member.data.get(data_id))
    member.network_socket.send(
        member.manager_id_chip, IDs.PQ2SQ_RESHARING_STEP, member.id
    )


def pq2sq_result_step(member, message_value):
    components = message_value.split(";")
    data_id = components[0]
    data_id_result = components[1]

    member.join_polynomial_shares(data_id, data_id_result)
    member.network_socket.send(member.manager_id_chip, IDs.PQ2SQ_RESULT_STEP, member.id)
