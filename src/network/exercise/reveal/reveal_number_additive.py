from src.network.exercise.exercise_class import Exercise
from src.globals import IDs

from functools import partial


def add_exercise_reveal_number_additive(manager, data_id):
    manager.exercises.append(
        Exercise(
            IDs.REVEAL_NUMBER_ADDITIVE,
            data_id,
            on_completion=partial(on_completion_reveal_number_additive),
        )
    )


def on_completion_reveal_number_additive(manager, exercise):
    manager.default_on_completion(exercise)
    value_to_send = 0
    if exercise.value.endswith("_0") and (manager.data.get(exercise.value) is not None):
        value_to_send = manager.data.get(exercise.value) % manager.prim_number
    manager.join_additive_shares(exercise.value)
    value_to_send = (
        value_to_send + manager.data.get(exercise.value)
    ) % manager.prim_number

    manager.send_to_all(exercise.value, value_to_send)
    manager.logger.info_spn(
        f"{exercise.value} is {value_to_send}. (from additive shares)"
    )


def reveal_number_additive(member, message_value):
    data_id = message_value
    member.network_socket.send(
        member.manager_id_chip, f"{data_id}_{member.id}", member.data.get(data_id)
    )
    member.network_socket.send(
        member.manager_id_chip, IDs.REVEAL_NUMBER_ADDITIVE, member.id
    )
