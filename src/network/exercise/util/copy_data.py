from src.network.exercise.exercise_class import Exercise
from src.globals import IDs


def add_exercise_copy_data(manager, data_id, data_id_result=None):
    if data_id_result is None:
        data_id_result = f"{data_id}_copy"
    manager.exercises.append(Exercise(IDs.COPY_DATA, f"{data_id};{data_id_result}"))


def copy_data(member, message_value):
    components = message_value.split(";")
    data_id = components[0]
    data_id_result = components[1]
    member.data[data_id_result] = member.data.get(data_id)
    member.network_socket.send(member.manager_id_chip, IDs.COPY_DATA, member.id)
