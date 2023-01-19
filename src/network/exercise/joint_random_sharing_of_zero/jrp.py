from src.network.exercise.exercise_class import Exercise
from src.globals import IDs
from src.network.exercise.math.addition import add_exercise_addition
from src.network.exercise.util.delete_data_at_ids import add_exercise_delete_data_at_ids
from src.network.exercise.util.manager_insert_in_share import (
    add_exercise_manager_insert_in_share,
)


def add_exercise_jrp(manager, value, data_id_result):

    data_id_zero = f"{data_id_result}_zero"

    manager.data[f"{data_id_result}"] = value
    add_exercise_manager_insert_in_share(manager, data_id_result)

    manager.exercises.append(Exercise(IDs.JRP_SHARING_STEP, f"{value};{data_id_zero}"))
    manager.exercises.append(Exercise(IDs.JRP_RESULT_STEP, data_id_zero))

    add_exercise_addition(manager, data_id_result, data_id_zero, data_id_result)
    add_exercise_delete_data_at_ids(manager, data_id_zero)


def jrp_sharing_step(member, message_value):
    components = message_value.split(";")
    value = int(components[0])
    data_id_result = components[1]

    member.insert_in_share(data_id_result, value)
    member.network_socket.send(member.manager_id_chip, IDs.JRP_SHARING_STEP, member.id)


def jrp_result_step(member, message_value):
    data_id_result = message_value
    member.join_polynomial_shares(data_id_result)
    member.network_socket.send(member.manager_id_chip, IDs.JRP_RESULT_STEP, member.id)
