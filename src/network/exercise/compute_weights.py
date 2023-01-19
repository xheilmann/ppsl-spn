from spn.structure.Base import get_nodes_by_type
from spn.structure.Base import Sum

from src.network.exercise.math.division import add_exercise_division

from src.network.exercise.util.delete_data_at_ids import add_exercise_delete_data_at_ids
from src.network.exercise.reveal.reveal_number import add_exercise_reveal_number

def add_exercise_compute_weights(manager):
    """
    exercise to compute the final sum weights
    """
    for structure_id in range(len(manager.spn)):
        
        data_ids_of_denominators = []
        spn = manager.spn[structure_id]
        sum_node_id = spn.id
        data_id_denominator = f"{structure_id}_({sum_node_id}, {sum_node_id})"
        data_ids_of_denominators.append(data_id_denominator)
        for child in spn.children:
            child_node_id = child.id
            data_id_numerator = f"{structure_id}_({sum_node_id}, {child_node_id})"
            add_exercise_division(
                    manager, data_id_numerator, data_id_denominator, data_id_numerator
                )
            #add_exercise_reveal_number(manager, data_id_numerator)
        ids_to_delete = ";".join(data_ids_of_denominators)
        add_exercise_delete_data_at_ids(manager, ids_to_delete)
