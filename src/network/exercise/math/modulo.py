import math
from src.network.exercise.exercise_class import Exercise
from src.globals import IDs, Values

from src.network.exercise.math.approx_inverse import add_exercise_approx_inverse
from src.network.exercise.math.trunc import add_exercise_trunc
from src.network.exercise.math.multiplication import add_exercise_multiplication
from src.network.exercise.math.subtraction import add_exercise_subtraction
from src.network.exercise.math.multiplicative_inverse import (
    add_exercise_multiplicative_inverse,
)

from src.network.exercise.reveal.reveal_number import add_exercise_reveal_number
from src.network.exercise.util.manager_insert_in_share import (
    add_exercise_manager_insert_in_share,
)

from functools import partial


def add_exercise_modulo(manager, data_id, data_id_of_modulant, data_id_result=None):
    add_exercise_modulo_cheating(manager, data_id, data_id_of_modulant, data_id_result)
    # self.add_exercise_modulo_paper(data_id,data_id_of_modulant, data_id_result)


def add_exercise_modulo_cheating(
    manager, data_id, data_id_of_modulant, data_id_result=None
):
    if data_id_result is None:
        data_id_result = data_id
    add_exercise_reveal_number(manager, data_id)
    add_exercise_reveal_number(manager, data_id_of_modulant)
    manager.exercises.append(
        Exercise(
            IDs.MODULO_CHEATING,
            f"{data_id};{data_id_of_modulant};{data_id_result}",
            on_completion=partial(on_completion_modulo_cheating, manager),
        )
    )
    add_exercise_manager_insert_in_share(manager, data_id_result)
    add_exercise_manager_insert_in_share(manager, data_id)
    add_exercise_manager_insert_in_share(manager, data_id_of_modulant)


def on_completion_modulo_cheating(manager, exercise):
    components = exercise.value.split(";")
    data_id = components[0]
    data_id_of_modulant = components[1]
    data_id_result = components[2]

    value = manager.data.get(data_id)
    value_of_modulant = manager.data.get(data_id_of_modulant)
    manager.data[data_id_result] = value % value_of_modulant
    manager.default_on_completion(exercise)


def modulo_cheating(member, message_value):
    member.network_socket.send(member.manager_id_chip, IDs.MODULO_CHEATING, member.id)


###################################################


def add_exercise_modulo_paper(
    manager, data_id, data_id_of_modulant, data_id_result=None
):
    if data_id_result is None:
        data_id_result = data_id
    k = manager.amount_members
    log_k = math.ceil(math.log(k, 2))
    n = manager.sharing_over_integer_allowed_bit_length_of_secret
    t = (
        math.floor(math.log(manager.prim_number, 2))
        - manager.sharing_over_integer_security_parameter
        - log_k
        - 6
        - n
    )

    parameter_L = (
        manager.sharing_over_integer_security_parameter
        + manager.sharing_over_integer_allowed_bit_length_of_secret
        + 6
        + t
        + 2 * math.ceil(math.log(k + 1, 2))
        - math.floor(math.log(manager.prim_number, 2))
    ) + 1

    error = (k + 1) * (1 + pow(2, n + 4 - n - t) + pow(2, parameter_L - n + 1))
    print(f"error = {error}")

    parameter_L = math.floor(math.log(manager.prim_number, 2))

    data_id_of_calculation = f"{data_id}_mod_{data_id_of_modulant}"

    data_id_of_approx_inverse_modulant = (
        f"{data_id_of_calculation}_approx_inverse_modulant"
    )
    data_id_trunc = f"{data_id_of_calculation}_trunc"
    data_id_q_trunc = f"{data_id_of_calculation}_q_trunc"
    data_id_q = f"{data_id_of_calculation}_q"
    data_id_tmp = f"{data_id_of_calculation}_tmp"

    add_exercise_approx_inverse(
        manager, data_id_of_modulant, data_id_of_approx_inverse_modulant
    )
    add_exercise_trunc(manager, data_id, parameter_L, data_id_trunc)

    add_exercise_multiplication(
        manager, data_id_trunc, data_id_of_approx_inverse_modulant, data_id_q_trunc
    )

    add_exercise_trunc(manager, data_id_q_trunc, n + t - parameter_L, data_id_q)

    add_exercise_multiplication(manager, data_id_of_modulant, data_id_q, data_id_tmp)

    add_exercise_subtraction(manager, data_id, data_id_tmp, data_id_result)


###################################################


def add_exercise_modulo_alt(manager, data_id, data_id_of_modulant, data_id_result=None):
    add_exercise_reveal_number(manager, data_id_of_modulant)
    add_exercise_multiplicative_inverse(manager, data_id_of_modulant)
    data_id_of_inverse_modulant = f"{data_id_of_modulant}_inverse"
    add_exercise_reveal_number(manager, data_id_of_inverse_modulant)
    add_exercise_multiplication(
        manager, data_id, data_id_of_inverse_modulant, f"{data_id}_mod_q"
    )
    add_exercise_reveal_number(manager, f"{data_id}_mod_q")
    add_exercise_multiplication(
        manager,
        data_id_of_modulant,
        f"{data_id}_mod_q",
        f"{data_id}_mod_q_times_modulant",
    )
    add_exercise_reveal_number(manager, f"{data_id}_mod_q_times_modulant")
    if data_id_result is None:
        data_id_result = f"{data_id}_mod_{data_id_of_modulant}"
    add_exercise_subtraction(
        manager,
        data_id,
        f"{data_id}_mod_q_times_modulant",
        data_id_result,
    )
    add_exercise_reveal_number(manager, data_id_result)
