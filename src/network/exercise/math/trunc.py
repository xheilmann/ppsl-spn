from decimal import Decimal, getcontext
from functools import partial
import math
from src.network.exercise.exercise_class import Exercise
from src.globals import IDs

from src.network.exercise.conversion.pq2sq import add_exercise_pq2sq
from src.network.exercise.conversion.sq2si import add_exercise_sq2si
from src.network.exercise.conversion.si2sq import add_exercise_si2sq
from src.network.exercise.conversion.sq2pq import add_exercise_sq2pq
from src.network.exercise.joint_random_sharing_of_zero.jrpz import add_exercise_jrpz
from src.network.exercise.math.addition import add_exercise_addition
from src.network.exercise.math.multiplication import add_exercise_multiplication
from src.network.exercise.math.multiplication_with_clear_value import add_exercise_multiplication_with_clear_value

from src.network.exercise.math.subtraction import add_exercise_subtraction
from src.network.exercise.reveal.reveal_number import add_exercise_reveal_number
from src.network.exercise.util.delete_data_at_ids import add_exercise_delete_data_at_ids
from src.network.exercise.util.manager_insert_in_share import (
    add_exercise_manager_insert_in_share,
)

import random

def binaer(n,N=256):
    s = []
    n = n % 2**N
    while n>0:
        if n%2==1:
            s.insert(0,1)
            n -=1
        else:
            s.insert(0,0)
        n = n//2
    while len(s) < N:
        s.insert(0,0)
    return s

def compute_power(a,m,modu=10000000000000000000000000000000000000000000000000000):
    getcontext().prec = 100
    M = binaer(m,math.ceil(math.log2(modu))+1)
    z = a
    x = 1
    for i in range(len(M)-1,0,-1):
        if M[i]==1:
            x = int((Decimal(x)*Decimal(z)) % Decimal(modu))
        z = int((Decimal(z)*Decimal(z)) % Decimal(modu))
    return x

def add_exercise_trunc(manager, data_id, n, data_id_result=None):
    getcontext().prec = 100
    if data_id_result is None:
        data_id_result = data_id

    # r = random.randint(1, 1024)
    # s = pow(2, n)

    manager.exercises.append(
        Exercise(
            IDs.TRUNC_INIT,
            f"{data_id};{n};{data_id_result}",
            on_start=partial(on_start_trunc_init, manager),
        )
    )

    # r = random.randint(1, 1024)
    s = pow(2, n)
    #s = 1000000

    data_id_r = f"{data_id}_trunc_r"
    data_id_z = f"{data_id}_trunc_z"

    data_id_x_add_r = f"{data_id}_trunc_x_add_r"

    data_id_zero = f"{data_id}_trunc_zero"

    data_id_h = f"{data_id}_trunc_h"

    data_id_tmp = f"{data_id}_trunc_tmp"

    add_exercise_jrpz(manager, data_id_zero)
    # manager.data[data_id_r_value_to_add] = r
    add_exercise_manager_insert_in_share(manager, data_id_r)
    add_exercise_addition(manager, data_id_r, data_id_zero, data_id_r)

    # z = r % s
    add_exercise_manager_insert_in_share(manager, data_id_z)

    add_exercise_addition(manager, data_id, data_id_r, data_id_x_add_r)

    add_exercise_reveal_number(manager, data_id_x_add_r)
    # x_add_r_clear = manager.data.get(data_id_x_add_r)
    # h = x_add_r_clear % s

    manager.exercises.append(
        Exercise(
            IDs.TRUNC_H_STEP,
            f"{data_id};{n};{data_id_result}",
            on_start=partial(on_start_trunc_h_step, manager),
        )
    )

    # manager.data[data_id_h] = h
    add_exercise_manager_insert_in_share(manager, data_id_h)

    add_exercise_addition(manager, data_id, data_id_z, data_id_tmp)
    add_exercise_subtraction(manager, data_id_tmp, data_id_h, data_id_tmp)

    # manager.data[data_id_s_inv] = pow(s,manager.prim_number-2,manager.prim_number)
    # add_exercise_manager_insert_in_share(manager, data_id_s_inv)

    #add_exercise_multiplication(manager, data_id_tmp, data_id_s_inv, data_id_result)
    s_inverse = compute_power(s, manager.prim_number - 2, manager.prim_number) #pow(s, manager.prim_number - 2, manager.prim_number)
    add_exercise_multiplication_with_clear_value(manager, data_id_tmp, s_inverse, data_id_result)
    
    add_exercise_delete_data_at_ids(
        manager,
        data_id_r,
        #data_id_s_inv,
        data_id_z,
        data_id_x_add_r,
        data_id_zero,
        data_id_h,
        data_id_tmp,
    )

    # manager.exercises.append(
    #    Exercise(IDs.TRUNC, f"{data_id_tmp};{s};{data_id_result}")
    # )

    # add_exercise_reveal_number(manager, data_id_x_add_r)
    # data_id_x_add_r % s


def trunc_init(member, message_value):
    components = message_value.split(";")
    data_id = components[0]
    n = int(components[1])
    data_id_result = components[2]

    #data_id_s_inv = f"{data_id}_trunc_s_inv"
    #s = pow(2, n)
    #member.data[data_id_s_inv] = pow(s, member.prim_number - 2, member.prim_number)

    member.network_socket.send(member.manager_id_chip, IDs.TRUNC_INIT, member.id)


def on_start_trunc_init(manager, exercise):
    getcontext().prec = 100
    components = exercise.value.split(";")
    data_id = components[0]
    n = int(components[1])
    data_id_result = components[2]

    r = random.randint(1, manager.sharing_over_integer_max_secret)
    s = pow(2, n)
    #s_inv = pow(s, manager.prim_number - 2, manager.prim_number)
    z = r % s

    data_id_r = f"{data_id}_trunc_r"
    data_id_s = f"{data_id}_trunc_s"
    data_id_s_inv = f"{data_id}_trunc_s_inv"
    data_id_z = f"{data_id}_trunc_z"

    manager.data[data_id_r] = r
    manager.data[data_id_s] = s
    #manager.data[data_id_s_inv] = s_inv
    manager.data[data_id_z] = z
    # manager.send_to_all(data_id_s_inv, s_inv)

    manager.default_on_start(exercise)


def trunc_h_step(member, message_value):
    components = message_value.split(";")
    data_id = components[0]
    n = int(components[1])
    data_id_result = components[2]

    member.network_socket.send(member.manager_id_chip, IDs.TRUNC_H_STEP, member.id)


def on_start_trunc_h_step(manager, exercise):
    components = exercise.value.split(";")
    data_id = components[0]
    n = int(components[1])
    data_id_result = components[2]

    data_id_s = f"{data_id}_trunc_s"
    data_id_x_add_r = f"{data_id}_trunc_x_add_r"
    data_id_h = f"{data_id}_trunc_h"

    manager.data[data_id_h] = manager.data.get(data_id_x_add_r) % manager.data.get(
        data_id_s
    )

    manager.default_on_start(exercise)


def add_exercise_trunc_old(manager, data_id, n, data_id_result=None):
    if data_id_result is None:
        data_id_result = data_id
    add_exercise_pq2sq(manager, data_id, data_id_result)
    add_exercise_sq2si(manager, data_id_result)
    manager.exercises.append(
        Exercise(IDs.TRUNC, f"{data_id_result};{n};{data_id_result}")
    )
    add_exercise_si2sq(manager, data_id_result)
    add_exercise_sq2pq(manager, data_id_result)


def trunc_old(member, message_value):
    components = message_value.split(";")
    data_id = components[0]
    n = int(components[1])
    data_id_result = components[2]
    value = member.data.get(data_id)
    member.data[data_id_result] = math.trunc(Decimal(value) / Decimal(pow(2, n)))
    member.network_socket.send(member.manager_id_chip, IDs.TRUNC, member.id)
