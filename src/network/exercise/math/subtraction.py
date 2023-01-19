from src.network.exercise.exercise_class import Exercise
from src.globals import IDs

from decimal import Decimal
from decimal import getcontext

def add_exercise_subtraction(
    manager, data_id_to_sub_from, data_id_to_sub, data_id_result=None
):
    if data_id_result is None:
        data_id_result = data_id_to_sub_from
    manager.exercises.append(
        Exercise(
            IDs.SUBTRACTION,
            f"{data_id_to_sub_from};{data_id_to_sub};{data_id_result}",
        )
    )


def subtraction(member, message_value):
    getcontext().prec = 200
    components = message_value.split(";")
    data_id_to_sub_from = components[0]
    data_id_to_sub = components[1]
    data_id_result = components[2]
    member.data[data_id_result] = int((
        Decimal(member.data.get(data_id_to_sub_from))
        - Decimal(member.data.get(data_id_to_sub))
    ) % Decimal(member.prim_number)) % member.prim_number
    member.network_socket.send(member.manager_id_chip, IDs.SUBTRACTION, member.id)
