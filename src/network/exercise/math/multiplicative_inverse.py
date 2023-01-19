import math
from random import randint
from src.network.exercise.exercise_class import Exercise
from src.globals import IDs

from src.network.exercise.math.multiplication import add_exercise_multiplication
from src.network.exercise.reveal.reveal_number import add_exercise_reveal_number
from src.network.exercise.reveal.receive_revealed_value import (
    add_exercise_receive_revealed_value,
)
from decimal import Decimal, getcontext

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
    M = binaer(m, math.ceil(math.log2(modu))+1)
    z = a
    x = 1
    for i in range(len(M)-1,0,-1):
        if M[i]==1:
            x = int((Decimal(x)*Decimal(z)) % Decimal(modu))
        z = int((Decimal(z)*Decimal(z)) % Decimal(modu))
    return x

def add_exercise_multiplicative_inverse(manager, data_id, data_id_result=None):
    manager.exercises.append(Exercise(IDs.INVERSE_SHARING_R_STEP, data_id))
    manager.exercises.append(Exercise(IDs.INVERSE_JOINING_R_STEP, data_id))
    add_exercise_multiplication(
        manager, f"{data_id}", f"{data_id}_inverse_r", f"{data_id}_inverse_u"
    )
    add_exercise_reveal_number(manager, f"{data_id}_inverse_u")
    add_exercise_receive_revealed_value(manager, f"{data_id}_inverse_u")
    # self.send_to_all(f"{data_id}_inverse_u", self.data.get(f"{data_id}_inverse_u"))
    if data_id_result is None:
        data_id_result = f"{data_id}_inverse"
    manager.exercises.append(
        Exercise(IDs.INVERSE_RESULT_STEP, f"{data_id};{data_id_result}")
    )


def inverse_sharing_r_step(member, message_value):
    data_id = message_value
    assert member.data.get(data_id) != 0  # TODO: proofe
    r = randint(1, member.prim_number - 1)
    member.insert_in_share(f"{data_id}_inverse_r", r)
    member.network_socket.send(
        member.manager_id_chip, IDs.INVERSE_SHARING_R_STEP, member.id
    )


def inverse_joining_r_step(member, message_value):
    data_id = message_value
    member.join_polynomial_shares(f"{data_id}_inverse_r")
    member.network_socket.send(
        member.manager_id_chip, IDs.INVERSE_JOINING_R_STEP, member.id
    )


def inverse_result_step(member, message_value):
    getcontext().prec = 100
    components = message_value.split(";")
    data_id = components[0]
    data_id_result = components[1]
    u = member.data.get(f"{data_id}_inverse_u")
    r = member.data.get(f"{data_id}_inverse_r")
    u_inverse = compute_power(u, member.prim_number - 2, member.prim_number) #pow(u, member.prim_number - 2, member.prim_number) % member.prim_number
    member.data[data_id_result] = int(
        ((Decimal(r)) * Decimal(u_inverse)) % Decimal(member.prim_number)) % member.prim_number

    member.network_socket.send(
        member.manager_id_chip, IDs.INVERSE_RESULT_STEP, member.id
    )
    del member.data[f"{data_id}_inverse_u"]
    del member.data[f"{data_id}_inverse_r"]
