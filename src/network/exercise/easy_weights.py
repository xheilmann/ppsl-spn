from spn.structure.Base import get_nodes_by_type
from spn.structure.Base import Sum

from src import IDs
from src.network.exercise import add_exercise_insert_edge_usage
from src.network.exercise.exercise_class import Exercise
from src.network.exercise.math.division import add_exercise_division
from src.network.exercise.util.copy_data import add_exercise_copy_data

from src.network.exercise.util.delete_data_at_ids import add_exercise_delete_data_at_ids
from src.network.exercise.reveal.reveal_number import add_exercise_reveal_number


def add_exercise_easy_weights(manager):
    """
    exercise to define the sum weights for all sum nodes except the root node.
    """
    add_exercise_insert_edge_usage(manager)

    manager.exercises.append (Exercise(IDs.EASY_WEIGHTS))

def easy_weights(member, message_value):
    for structure_id in range(len(member.spn)):
        
    
    # adding the usages of one sumnode to child node together
        for sum_node in get_nodes_by_type(member.spn[structure_id], ntype=Sum):
            sum_node_id = sum_node.id
            if sum_node_id != 0:
                
                for child  in sum_node.children:
                    child_node_id = child.id
                    data_id_numerator = f"{structure_id}_({sum_node_id}, {child_node_id})"
                    member.data[data_id_numerator] = int(1/len(sum_node.children)*member.d_multiplyer)
                #for member_id in member.id_chips_for_id.keys():
                    #member.addTo(data_id_numerator, f"{data_id_numerator}_{member_id}")
                    #del member.data[f"{data_id_numerator}_{member_id}"]
    
        # adding the usages of all childs of a sum node together (as denominator)
        #for sum_node in get_nodes_by_type(member.spn[structure_id], ntype=Sum):
            #sum_node_id = sum_node.id
            #if sum_node_id != 0:
                
                #data_id_denominator = f"{structure_id}_({sum_node_id}, {sum_node_id})"
                #member.data[data_id_denominator] = 0
                #child_node_id = sum_node.children[0].id
                #for child in sum_node.children:
                    #member.addTo(data_id_denominator, f"{structure_id}_({sum_node_id}, {child_node_id})")



    member.network_socket.send(
        member.manager_id_chip, IDs.EASY_WEIGHTS, member.id
    )

