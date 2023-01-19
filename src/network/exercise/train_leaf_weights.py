import itertools

import numpy as np
import csv

from scipy.special import logsumexp
from spn.algorithms.Inference import likelihood, log_likelihood
from spn.structure.leaves.parametric.EM import add_parametric_EM_support

from src.network.exercise.exercise_class import Exercise
from src.globals import IDs, Keys

from spn.structure.Base import get_nodes_by_type, Leaf
from spn.structure.Base import Sum
from spn.algorithms.EM import EM_optimization

from spn.algorithms.Gradient import gradient_backward
from spn.structure.Base import get_number_of_nodes


def add_exercise_train_leaf_weights(manager):
    """
    exercise to share the local leaf parameters with all other members
    """
    #string = " ".join(map(str,leaf_stats))
    manager.exercises.append(Exercise(IDs.TRAIN_LEAF_WEIGHTS))



def train_leaf_weights(member, message_value):
    for structure_id in range(len(member.spn)):
        structure = member.spn[structure_id]
        #print(components[2])
        for leaf in get_nodes_by_type(structure, ntype=Leaf):
            leafid = leaf.id
            data_id_p = f"{structure_id}_({leafid}, {leafid})_p"
            value_p = int(( member.d_multiplyer * leaf.p)/len(member.id_chips_for_id))
            data_id_p_inverse = f"{structure_id}_({leafid}, {leafid})_(1-p)"
            value_p_inverse = int((member.d_multiplyer - ( member.d_multiplyer * leaf.p))/len(member.id_chips_for_id))
            #member.data[data_id_p] = value_p
            #member.data[data_id_p_inverse] = value_p_inverse
            member.insert_in_share(data_id_p, value_p)
            member.insert_in_share(data_id_p_inverse, value_p_inverse)
            #print(f"id {member.id} for {data_id_p} we got value {value_p} and scope {leaf.scope}")
            #print(f"id {member.id} for {data_id_p_inverse} we got value {value_p_inverse} and scope {leaf.scope}")
    member.network_socket.send(
        member.manager_id_chip, IDs.TRAIN_LEAF_WEIGHTS, member.id)




