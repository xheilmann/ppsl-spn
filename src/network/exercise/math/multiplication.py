from src.network.exercise.exercise_class import Exercise
from src.globals import IDs
import numpy as np
import math
from decimal import Decimal
from decimal import getcontext


def add_exercise_multiplication(
    manager, data_id_a, data_id_b, data_id_result=None, divide_with_d=False, exponentiate=False, evaluation_mode=False
):
    if data_id_result is None:
        data_id_result = data_id_a
    if exponentiate:
        manager.exercises.append(
            Exercise(
                IDs.MULTIPLICATION_INTERMEDIATE_STEP,
                f"{data_id_a};{data_id_b};{data_id_result};true;false",
            )
        )
    if evaluation_mode:
        manager.exercises.append(
            Exercise(
                IDs.MULTIPLICATION_INTERMEDIATE_STEP,
                f"{data_id_a};{data_id_b};{data_id_result};false;true",
            )
        )
    else:
        manager.exercises.append(
            Exercise(
                IDs.MULTIPLICATION_INTERMEDIATE_STEP,
                f"{data_id_a};{data_id_b};{data_id_result};false;false",
            )
        )
    manager.exercises.append(
        Exercise(IDs.MULTIPLICATION_RESULT_STEP, f"{data_id_result};{divide_with_d}")
    )


def multiplication_intermediate_step(member, message_value):
    getcontext().prec = 200
    components = message_value.split(";")
    data_id_a = components[0]
    data_id_b = components[1]
    data_id_result = components[2]
    exponentiate = components[3]
    evaluation_mode = components[4]

    value_a = member.data.get(data_id_a)
    value_b = member.data.get(data_id_b)

    if exponentiate == "true":
        product = ((np.exp(float(value_a))) * value_b)
        if np.isinf(product):
            product = 1 % member.prim_number
        else:
            product = math.floor(product) % member.prim_number
    if evaluation_mode == "true":
        product = ((value_a * value_b) // 100) % member.prim_number
    else:
        product = int((Decimal(value_a) * Decimal(value_b)) % Decimal(member.prim_number) % member.prim_number)

    member.insert_in_share(f"{data_id_result}_intermediate", int(product))
    member.network_socket.send(
        member.manager_id_chip, IDs.MULTIPLICATION_INTERMEDIATE_STEP, member.id
    )


def multiplication_result_step(member, message_value):
    getcontext().prec = 200
    components = message_value.split(";")
    data_id_result = components[0]
    divide_with_d = components[1] in ["True", "true"]
    member.join_polynomial_shares(f"{data_id_result}_intermediate", data_id_result)
    if divide_with_d:
        member.data[data_id_result] = int((
            Decimal(member.data.get(data_id_result))
            * Decimal(member.d_multiplyer_inverse)
        ) % Decimal(member.prim_number)) % member.prim_number
    member.network_socket.send(
        member.manager_id_chip, IDs.MULTIPLICATION_RESULT_STEP, member.id
    )
