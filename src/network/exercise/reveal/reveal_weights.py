from spn.structure.Base import Sum, get_nodes_by_type, Leaf

from src.network.exercise.reveal.reveal_number import add_exercise_reveal_number


def add_exercise_reveal_weights(manager, structure_id):
    """
    reveals all privately learned parameters
    """
    data_id_weight = f"loglikl_weight_{structure_id}"
    data_id_weight_r = f"ranking_weight_{structure_id}"
    data_id_weight_enf = f"enf_loglikl_weight_{structure_id}"
    add_exercise_reveal_number(manager, data_id_weight)
    add_exercise_reveal_number(manager, data_id_weight_r)
    add_exercise_reveal_number(manager, data_id_weight_enf)
    
        
    for child in manager.spn[structure_id].children:
        sum_node_id = manager.spn[structure_id].id
        child_node_id = child.id
        data_id_numerator = f"{structure_id}_({sum_node_id}, {child_node_id})"
        add_exercise_reveal_number(manager, data_id_numerator)
    for leaf in get_nodes_by_type(manager.spn[structure_id], ntype=Leaf):
        data_id_p = f"{structure_id}_({leaf.id}, {leaf.id})_p"
        add_exercise_reveal_number(manager, data_id_p)
        data_id = f"{structure_id}_({leaf.id}, {leaf.id})_(1-p)"
        add_exercise_reveal_number(manager, data_id)
