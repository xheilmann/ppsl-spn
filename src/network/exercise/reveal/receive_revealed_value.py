from src.network.exercise.exercise_class import Exercise
from src.globals import IDs

from functools import partial


def add_exercise_receive_revealed_value(manager, data_id):
    # The real value to be reveled will be appended with ; at the data_id
    manager.exercises.append(
        Exercise(
            IDs.RECEIV_REVEALED_VALUE,
            data_id,
            on_start=partial(on_start_receive_revealed_value, manager),
        )
    )


def on_start_receive_revealed_value(member, exercise):
    data_id = exercise.value
    revealed_value = member.data.get(data_id)
    exercise.set_value(f"{data_id};{revealed_value}")
    member.default_on_start(exercise)
    del member.data[data_id]


def receive_revealed_value(member, message_value):
    components = message_value.split(";")
    data_id_of_revealed = components[0]
    revealed_value = components[1]
    member.data[data_id_of_revealed] = int(revealed_value)
    member.network_socket.send(
        member.manager_id_chip, IDs.RECEIV_REVEALED_VALUE, member.id
    )
