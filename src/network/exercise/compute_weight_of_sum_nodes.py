from src.network.exercise.exercise_class import Exercise
from src.globals import IDs

from spn.structure.Base import get_nodes_by_type
from spn.structure.Base import Sum


def add_exercise_compute_weight_of_sum_nodes(manager):
    """
    exercise to prepare the calculation of sum weights
    """
    manager.exercises.append(Exercise(IDs.COMPUTE_WEIGHT_OF_SUM_NODES))


def compute_weight_of_sum_nodes(member, message_value):
    for structure_id in range(len(member.spn)):
       
        spn = member.spn[structure_id]
        sum_node_id = spn.id
        for child in spn.children:
            child_node_id = child.id
            data_id_numerator = f"{structure_id}_({sum_node_id}, {child_node_id})"
            member.data[data_id_numerator] = 0
            for member_id in member.id_chips_for_id.keys():
                member.addTo(data_id_numerator, f"{data_id_numerator}_{member_id}")
                del member.data[f"{data_id_numerator}_{member_id}"]
    
        # adding the usages of all childs of a sum node together (as denominator)
        data_id_denominator = f"{structure_id}_({sum_node_id}, {sum_node_id})"
        member.data[data_id_denominator] = 0
        for child in spn.children:
            child_node_id = child.id
            member.addTo(data_id_denominator, f"{structure_id}_({sum_node_id}, {child_node_id})")

    member.network_socket.send(
        member.manager_id_chip, IDs.COMPUTE_WEIGHT_OF_SUM_NODES, member.id
    )