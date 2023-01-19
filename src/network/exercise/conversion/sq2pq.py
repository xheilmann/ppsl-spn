from src.network.exercise.exercise_class import Exercise
from src.globals import IDs


def add_exercise_sq2pq(manager, data_id, data_id_result=None):
    if data_id_result is None:
        data_id_result = data_id
    manager.exercises.append(Exercise(IDs.SQ2PQ_RESHARING_STEP, data_id))
    manager.exercises.append(
        Exercise(IDs.SQ2PQ_RESULT_STEP, f"{data_id};{data_id_result}")
    )


def sq2pq_resharing_step(member, message_value):
    data_id = message_value
    member.insert_in_share(data_id, member.data.get(data_id))
    member.network_socket.send(
        member.manager_id_chip, IDs.SQ2PQ_RESHARING_STEP, member.id
    )


def sq2pq_result_step(member, message_value):
    components = message_value.split(";")
    data_id = components[0]
    data_id_result = components[1]

    member.join_additive_shares(data_id, data_id_result)
    member.network_socket.send(member.manager_id_chip, IDs.SQ2PQ_RESULT_STEP, member.id)
