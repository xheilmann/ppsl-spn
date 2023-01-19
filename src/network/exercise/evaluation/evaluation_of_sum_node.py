from src.network.exercise.math.division import add_exercise_division_with_d_multiplyer
from src.network.exercise.reveal.reveal_number import add_exercise_reveal_number
from spn.structure.Base import Sum

from src.network.exercise.math.multiplication import add_exercise_multiplication
from src.network.exercise.math.addition import add_exercise_addition
from src.network.exercise.math.multiplication_with_clear_value import add_exercise_multiplication_with_clear_value
from src.network.exercise.util.copy_data import add_exercise_copy_data
from src.network.exercise.util.delete_data_at_ids import add_exercise_delete_data_at_ids


def add_exercise_evaluation_of_sum_node(manager, sum_node: Sum, structure_id):
    """
    evaluates the value of a single sum node
    :param manager: manager in network
    :param sum_node: sum node in structure
    :param structure_id: id of the structure in the forest
    """
    data_id_result = f"{structure_id}_({sum_node.id}, {sum_node.id})_result"

    manager.data[data_id_result] = 0
    data_ids_to_delete = []
    if sum_node.id ==0: 
        for index in range(len(sum_node.children)):
            child_node = sum_node.children[index]
            data_id_weight = f"{structure_id}_({sum_node.id}, {child_node.id})"
            data_id_child_result = f"{structure_id}_({child_node.id}, {child_node.id})_result"
    
            data_id_child_times_weight = f"{structure_id}_({sum_node.id}, {child_node.id})_times_({child_node.id}, {child_node.id})_result"
            #add_exercise_reveal_number(manager, data_id_weight)
            add_exercise_multiplication(
                manager,
                data_id_weight,
                data_id_child_result,
                data_id_child_times_weight,
                #from_own_data = True, 
                #float_type = False
            )
            #add_exercise_reveal_number(manager, data_id_child_times_weight)
            #add_exercise_division_with_d_multiplyer(
              #manager, data_id_child_times_weight, data_id_child_times_weight
            #)
            #add_exercise_reveal_number(manager, data_id_child_result)
            #add_exercise_reveal_number(manager, data_id_weight)
            
            
            
            if index == 0:
                add_exercise_copy_data(manager, data_id_child_times_weight, data_id_result)
            else:
                add_exercise_addition(
                    manager, data_id_result, data_id_child_times_weight, data_id_result
                )
            #add_exercise_reveal_number(manager, data_id_child_times_weight)
            data_ids_to_delete.append(data_id_child_times_weight)
    else: 
        #for index in range(len(sum_node.children)):
            #child_node = sum_node.children[index]
            #data_id_weight = f"{structure_id}_({sum_node.id}, {child_node.id})"
        child_node = sum_node.children[0]
        data_id_child_result = f"{structure_id}_({child_node.id}, {child_node.id})_result"
    
            #data_id_child_times_weight = f"{structure_id}_({sum_node.id}, {child_node.id})_times_({child_node.id}, {child_node.id})_result"
        add_exercise_copy_data(manager, data_id_child_result, data_id_result) 
    #add_exercise_division_with_d_multiplyer(
        #manager, data_id_result, data_id_result
    #)
    #add_exercise_reveal_number(manager, data_id_result)
    division_counter = f"{structure_id}_division_counter"
    manager.data[division_counter] = manager.data.get(division_counter) + 1
    if len(data_ids_to_delete) >0:
        add_exercise_delete_data_at_ids(manager, data_ids_to_delete)
