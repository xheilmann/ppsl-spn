from src.network.exercise.exercise_class import Exercise
from src.globals import IDs
import math
import numpy as np
from decimal import Decimal
from decimal import getcontext


def add_exercise_addition(manager, data_id_a, data_id_b, data_id_result = None, log = False):
    if data_id_result is None:
        data_id_result = data_id_a

    if log:
        manager.exercises.append(
            Exercise(IDs.ADDITION, f"{data_id_a};{data_id_b};{data_id_result};true")
        )
    else:
        manager.exercises.append(
            Exercise(IDs.ADDITION, f"{data_id_a};{data_id_b};{data_id_result};false")
        )


def addition(member, message_value):
    components = message_value.split(";")
    data_id_a = components[0]
    data_id_b = components[1]
    data_id_result = components[2]
    log_param = components[3]

    if log_param == "true":
        result = np.log(float(member.data.get(data_id_a) + member.data.get(data_id_b)))
        if np.isinf(result):
            result = 1 % member.prim_number
        else:
            result = math.floor(abs(result)) % member.prim_number
        member.data[data_id_result] = result
    else:
        getcontext().prec = 100
        member.data[data_id_result] = int((
            Decimal(member.data.get(data_id_a)) + Decimal(member.data.get(data_id_b))
        ) % Decimal(member.prim_number)) % member.prim_number
    member.network_socket.send(member.manager_id_chip, IDs.ADDITION, member.id)
