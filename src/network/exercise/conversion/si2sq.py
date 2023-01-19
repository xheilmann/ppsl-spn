from src.network.exercise.exercise_class import Exercise
from src.globals import IDs


def add_exercise_si2sq(manager, data_id, data_id_result=None):
    if data_id_result is None:
        data_id_result = data_id
    manager.exercises.append(Exercise(IDs.SI2SQ, f"{data_id};{data_id_result}"))


def si2sq(member, message_value):
    components = message_value.split(";")
    data_id = components[0]
    data_id_result = components[1]

    member.data[data_id_result] = member.data.get(data_id) % member.prim_number
    member.network_socket.send(member.manager_id_chip, IDs.SI2SQ, member.id)
