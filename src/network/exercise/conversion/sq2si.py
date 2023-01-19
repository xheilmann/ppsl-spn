import math
from src.network.exercise.exercise_class import Exercise
from src.globals import IDs, Values

from src.network.exercise.joint_random_sharing_of_zero.jriz import add_exercise_jriz
from src.network.exercise.util.delete_data_at_ids import add_exercise_delete_data_at_ids

from decimal import Decimal


def add_exercise_sq2si(manager, data_id, data_id_result=None):
    if data_id_result is None:
        data_id_result = data_id
    manager.exercises.append(Exercise(IDs.SQ2SI_SHARING_STEP, data_id))
    add_exercise_jriz(manager, f"{data_id}_sq2si_jriz")
    manager.exercises.append(
        Exercise(IDs.SQ2SI_RESULT_STEP, f"{data_id};{data_id_result}")
    )
    add_exercise_delete_data_at_ids(manager, f"{data_id}_sq2si_jriz")


def sq2si_sharing_step(member, message_value):
    data_id = message_value

    t = (
        2
        + member.sharing_over_integer_security_parameter
        + member.sharing_over_integer_allowed_bit_length_of_secret
    )
    value = member.data.get(data_id)
    value_decimal = Decimal(value)
    value_decimal = value_decimal / Decimal(pow(2, t))
    if value < 0:
        value_trunc = math.ceil(value_decimal)
    else:
        value_trunc = math.floor(value_decimal)
    member.insert_in_share_clear(f"{data_id}_sq2si_trunc", value_trunc)
    member.network_socket.send(
        member.manager_id_chip, IDs.SQ2SI_SHARING_STEP, member.id
    )


def sq2si_result_step(member, message_value):
    components = message_value.split(";")
    data_id = components[0]
    data_id_result = components[1]

    t = (
        2
        + member.sharing_over_integer_security_parameter
        + member.sharing_over_integer_allowed_bit_length_of_secret
    )
    data_id_sum_of_trun = f"{data_id}_sq2si_sum_of_trunc"
    member.join_additive_integer_shares(f"{data_id}_sq2si_trunc", data_id_sum_of_trun)
    id_to_switch = (
        pow(2, t) * member.data.get(data_id_sum_of_trun)
    ) / member.prim_number
    del member.data[data_id_sum_of_trun]

    id_to_switch_rounded = round(id_to_switch)  # wrong for x.5000...
    own_share_of_zero = member.data.get(f"{data_id}_sq2si_jriz")

    value_to_set = member.data.get(data_id) + own_share_of_zero
    if int(member.id) <= abs(id_to_switch_rounded):
        if id_to_switch_rounded > 0:
            value_to_set -= member.prim_number
        else:
            value_to_set += member.prim_number

    member.data[data_id_result] = value_to_set
    member.network_socket.send(member.manager_id_chip, IDs.SQ2SI_RESULT_STEP, member.id)
