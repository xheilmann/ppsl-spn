import math

import numpy as np
from spn.structure.Base import Product, Sum, Leaf

from src import DataIDs
from src.network.exercise.math.addition import add_exercise_addition
from src.network.exercise.util.copy_data import add_exercise_copy_data
from src.network.exercise.math.multiplication import add_exercise_multiplication
from src.network.exercise.math.multiplication_with_clear_value import add_exercise_multiplication_with_clear_value
from src.network.exercise.math.division import (
    add_exercise_division,
    add_exercise_division_with_d_multiplyer,
)
from src.network.exercise.math.multiplication_with_clear_value import (
    add_exercise_multiplication_with_clear_value,
)
from src.network.exercise.reveal.reveal_number import add_exercise_reveal_number
from src.network.exercise.util.dummy import add_exercise_dummy


def add_exercise_evaluation_of_product_node(manager, product_node: Product, structure_id):
    """

    evaluates the value of a single product node
    :param manager: manager in network
    :param product_node:  product node in structure
    :param structure_id: id of the structure in the forest

    """
    data_id_result = f"{structure_id}_({product_node.id}, {product_node.id})_result"
    #add_exercise_dummy(manager)
    #division_counter = f"{structure_id}_division_counter"
    #manager.data[division_counter] = 0
    division_counter = 0
    sum_counter = 0
    max_division_times = math.floor(100/math.log(manager.prim_number, 10)) - 1
    for index in range(len(product_node.children)):
        
        child_node = product_node.children[index]
        #print(isinstance(child_node, Leaf))
        data_id_child_result = f"{structure_id}_({child_node.id}, {child_node.id})_result"
        #if type(child_node) == Sum:
            #sum_counter += 1
           
        if isinstance(child_node, Leaf):
            #print("true")
            data_id_p = f"{structure_id}_({child_node.id}, {child_node.id})_p_result"
            data_id_leaf_weight_p = f"{structure_id}_({child_node.id}, {child_node.id})_p"
            data_id_p_inverse = f"{structure_id}_({child_node.id}, {child_node.id})_(1-p)_result"
            data_id_leaf_weight_p_inverse = f"{structure_id}_({child_node.id}, {child_node.id})_(1-p)"
            add_exercise_multiplication(
                manager,
                data_id_p,
                data_id_leaf_weight_p,
                data_id_p
            
            )
            add_exercise_multiplication(
                manager,
                data_id_p_inverse,
                data_id_leaf_weight_p_inverse,
                data_id_p_inverse
                
            )
            
            add_exercise_addition(
                manager, 
                data_id_p,
                data_id_p_inverse,
                data_id_child_result)
            
           
        if index == 0:
            add_exercise_copy_data(manager, data_id_child_result, data_id_result)
            #add_exercise_reveal_number(manager, data_id_child_result)
        else:
            
            add_exercise_multiplication(
                manager,
                data_id_result,
                data_id_child_result,
                data_id_result,
                divide_with_d=False,
                evaluation_mode=False
            )
            #add_exercise_reveal_number(manager, data_id_result)
            #add_exercise_reveal_number(manager, data_id_child_result)
            division_counter += 1
            if division_counter + sum_counter >= max_division_times:
                #add_exercise_reveal_number(manager, data_id_result)
                #print(division_counter)
                add_exercise_division_with_d_multiplyer(
                manager,
                data_id_result,
                data_id_result, 
                times = division_counter       
            )
                sum_counter = 0
                division_counter = 0
                #add_exercise_reveal_number(manager, data_id_result)
    add_exercise_division_with_d_multiplyer(
                manager,
                data_id_result,
                data_id_result, 
                times = division_counter       
            )
            #add_exercise_division_with_d_multiplyer(
             # manager, data_id_result, data_id_result, times=1
            #)
            #add_exercise_multiplication_with_clear_value(
             #   manager,
              #  data_id_result,
               # pow(manager.d_multiplyer, manager.prim_number-2, manager.prim_number),
                #data_id_result            
            #)
            
            #manager.data[division_counter] = manager.data.get(division_counter) + 1
            
        #add_exercise_reveal_number(manager, data_id_child_result)
    #add_exercise_reveal_number(manager, data_id_result)
    '''
    if manager.data.get(division_counter) != 0:
        manager.data[division_counter] = manager.d_multiplyer ** (manager.data.get(division_counter)-1)
        add_exercise_copy_data(manager, division_counter, division_counter)
        add_exercise_division(
            manager, data_id_result, division_counter, data_id_result
        )
    
    '''
    
    
    #add_exercise_multiplication_with_clear_value(
       #         manager,
      #          data_id_result,
      #          1/(manager.d_multiplyer**((sum_counter +division_counter))),
      #          data_id_result, 
      #          from_own_data = False,
      #          float_type = True            
     #   )
    
    
    
    #add_exercise_reveal_number(manager, data_id_result)

    # self.add_exercise_multiplication_with_clear_value
