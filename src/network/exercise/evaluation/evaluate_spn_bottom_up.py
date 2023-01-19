from spn.structure.Base import Leaf, Product, Sum, get_topological_order
from src.network.exercise.math.multiplication import add_exercise_multiplication
from src.network.exercise.math.multiplication_with_clear_value import add_exercise_multiplication_with_clear_value

from src.network.exercise.evaluation.evaluation_of_sum_node import (
    add_exercise_evaluation_of_sum_node,
)
from src.network.exercise.evaluation.evaluation_of_product_node import (
    add_exercise_evaluation_of_product_node,
)


def add_exercise_evaluate_spn_bottom_up(manager, structure_id):
    """
    Evaluates the spn bottom up
    """
    division_counter = f"{structure_id}_division_counter"
    manager.data[division_counter] = 0
    for node in get_topological_order(manager.spn[structure_id]):
        if isinstance(node, Leaf):
            # self.add_exercise_evaluation_of_leaf_node(node)
            continue
        elif isinstance(node, Sum):
            add_exercise_evaluation_of_sum_node(manager, node, structure_id)
        elif isinstance(node, Product):
            add_exercise_evaluation_of_product_node(manager, node, structure_id)
        else:
            raise AssertionError(
                f"Evaluation of node type {node.__class__.__name__} not supported"
            )
    data_id_result = f"{structure_id}_(0, 0)_result"
    data_id_structure_weight = f"ranking_weight_{structure_id}"
    
    add_exercise_multiplication(
            manager,
            data_id_result,
            data_id_structure_weight,
            data_id_result,
            #from_own_data = True
            # float_type = False
    )
