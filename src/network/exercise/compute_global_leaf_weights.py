import numpy as np
import csv

from scipy.special import logsumexp
from spn.algorithms.Inference import likelihood, log_likelihood
from spn.structure.leaves.parametric.EM import add_parametric_EM_support

from src.network.exercise import add_exercise_reveal_number
from src.network.exercise.exercise_class import Exercise
from src.globals import IDs, Keys

from spn.structure.Base import get_nodes_by_type, Leaf
from spn.structure.Base import Sum
from spn.algorithms.EM import EM_optimization

from spn.algorithms.Gradient import gradient_backward
from spn.structure.Base import get_number_of_nodes


def add_exercise_compute_global_leaf_weights(manager):
    """
    exercise to create the global leaf parameters from the shares of the locally trained leaf parameters
    """
    manager.exercises.append(Exercise(IDs.COMPUTE_GLOBAL_LEAF_WEIGHTS))
    #for structure_id in range(len(manager.spn)):
        #structure = manager.spn[structure_id]
        #for leaf in get_nodes_by_type(structure, ntype=Leaf):
            #data_id_p = f"{structure_id}_({leaf.id}, {leaf.id})_p"
            #add_exercise_reveal_number(manager, data_id_p)
            #data_id = f"{structure_id}_({leaf.id}, {leaf.id})_(1-p)"
            #add_exercise_reveal_number(manager, data_id)


def compute_global_leaf_weights(member, message_value):
    for structure_id in range(len(member.spn)):
        structure = member.spn[structure_id]
    
        for leaf in get_nodes_by_type(structure, ntype=Leaf):
            data_id_p = f"{structure_id}_({leaf.id}, {leaf.id})_p"
            data_id_p_inverse = f"{structure_id}_({leaf.id}, {leaf.id})_(1-p)"
            member.data[data_id_p] = 0
            member.data[data_id_p_inverse] = 0
            for member_id in member.id_chips_for_id.keys():
                member.addTo(data_id_p, f"{data_id_p}_{member_id}")
                del member.data[f"{data_id_p}_{member_id}"]
                member.addTo(data_id_p_inverse, f"{data_id_p_inverse}_{member_id}")
                del member.data[f"{data_id_p_inverse}_{member_id}"]

    member.network_socket.send(
        member.manager_id_chip, IDs.COMPUTE_GLOBAL_LEAF_WEIGHTS, member.id)