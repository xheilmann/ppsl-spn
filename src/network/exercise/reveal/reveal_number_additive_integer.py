from src.network.exercise.exercise_class import Exercise
from src.globals import IDs

from functools import partial


def add_exercise_reveal_number_additive_integer(manager, data_id):
    manager.exercises.append(
        Exercise(
            IDs.REVEAL_NUMBER_ADDITIVE_INTEGER,
            data_id,
            on_completion=partial(
                on_completion_reveal_number_additive_integer, manager
            ),
        )
    )


def on_completion_reveal_number_additive_integer(manager, exercise):
    manager.default_on_completion(exercise)

    manager.join_additive_integer_shares(exercise.value)
    value_to_send = manager.data.get(exercise.value)
    manager.send_to_all(exercise.value, value_to_send)
    manager.logger.info_spn(
        f"{exercise.value} is {value_to_send}. (from additive integer shares)"
    )
    print(f"{exercise.value} is {value_to_send}. (from additive integer shares)")


def reveal_number_additive_integer(member, message_value):
    data_id = message_value
    member.network_socket.send(
        member.manager_id_chip, f"{data_id}_{member.id}", member.data.get(data_id)
    )
    member.network_socket.send(
        member.manager_id_chip, IDs.REVEAL_NUMBER_ADDITIVE_INTEGER, member.id
    )
