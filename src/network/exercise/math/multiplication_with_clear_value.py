from src.network.exercise.exercise_class import Exercise
from src.globals import IDs
import math
from decimal import Decimal
from decimal import getcontext


def add_exercise_multiplication_with_clear_value(
    manager, data_id, value, data_id_result=None, from_own_data=False, float_type=False
):
    
    if from_own_data:
        if data_id_result is None:
            data_id_result = data_id
        manager.exercises.append(
          Exercise(
              IDs.MULTIPLICATION_WITH_CLEAR_VALUE,
              f"{data_id};{value};{data_id_result};true;false"
          )
          )
    elif float_type and not from_own_data:
        if data_id_result is None:
            data_id_result = data_id
        manager.exercises.append(
          Exercise(
              IDs.MULTIPLICATION_WITH_CLEAR_VALUE,
              f"{data_id};{value};{data_id_result};false;true"
          )
          )
    else:
        if data_id_result is None:
            data_id_result = data_id
        manager.exercises.append(
          Exercise(
              IDs.MULTIPLICATION_WITH_CLEAR_VALUE,
              f"{data_id};{value};{data_id_result};false;false"
          )
        )
    


def multiplication_with_clear_value(member, message_value):
    getcontext().prec = 100
    components = message_value.split(";")
    data_id = components[0]
    data_id_result = components[2]
    if components[3] == "false":
        if components[4] == "true": 
            value = float(components[1])
            member.data[data_id_result] = int((
              Decimal(member.data.get(data_id)) * Decimal(value)
            ) % Decimal(member.prim_number)) % member.prim_number
        else: 
            value = int(components[1])
            member.data[data_id_result] = int((
              Decimal(member.data.get(data_id)) * Decimal(value)
            ) % Decimal(member.prim_number)) % member.prim_number
    else:
        value = (member.data.get(components[1]))/(member.d_multiplyer)
        print(value)
        member.data[data_id_result] = int((
            Decimal(member.data.get(data_id)) * Decimal(value)
        ) % Decimal(member.prim_number)) % member.prim_number
        print(member.data.get(data_id_result))
    member.network_socket.send(
        member.manager_id_chip, IDs.MULTIPLICATION_WITH_CLEAR_VALUE, member.id
    )
