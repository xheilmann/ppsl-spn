from spn.structure.Base import Sum, get_nodes_by_type, Leaf
from src.network.exercise.exercise_class import Exercise
from src.globals import IDs, Keys


def add_exercise_save_spn_weights_to_file(manager, structure_id):
    """
    Optional method to save parameters to file to load for later inference
    """
    manager.exercises.append(Exercise(IDs.SAVE_SPN_WEIGHTS_TO_FILE, structure_id))


def save_spn_weights_to_file(member, message_value):
    structure_id = message_value
    spn_weights_file_path = member.config[f"ID_{member.id}"].get(
        Keys.CONFIG_SPN_WEIGHTS_FILE_PATH
    )
    f = open(spn_weights_file_path + f"/structure_{structure_id}", "w")

    #save structure weight vector
    data_id_weight = f"loglikl_weight_{structure_id}"
    data_id_weight_r = f"ranking_weight_{structure_id}"
    data_id_weight_enf = f"enf_loglikl_weight_{structure_id}"
    if data_id_weight in member.data:
        value = member.data.get(data_id_weight)
        f.write(f"{data_id_weight}={value}\n")
    if data_id_weight_r in member.data:
        value = member.data.get(data_id_weight_r)
        f.write(f"{data_id_weight_r}={value}\n")
    if data_id_weight_enf in member.data:
        value = member.data.get(data_id_weight_enf)
        f.write(f"{data_id_weight_enf}={value}\n")

    #save sum weights
    for sum_node in get_nodes_by_type(member.spn[structure_id], Sum):
        for child_node in sum_node.children:
            data_id_weight = f"{structure_id}_({sum_node.id}, {child_node.id})"
            value = member.data.get(data_id_weight)
            f.write(f"{data_id_weight}={value}\n")
    
    #save leaf weights
    
    for leaf in get_nodes_by_type(member.spn[structure_id], Leaf):
        data_id_p = f"{structure_id}_({leaf.id}, {leaf.id})_p"
        data_id_p_inverse = f"{structure_id}_({leaf.id}, {leaf.id})_(1-p)"
        value_p = member.data.get(data_id_p)
        value_p_inverse = member.data.get(data_id_p_inverse)
        f.write(f"{data_id_p}={value_p}\n")
        f.write(f"{data_id_p_inverse}={value_p_inverse}\n")
    
    f.close()
    #print(member.data)
    #print(member.used_edges)
    member.network_socket.send(
        member.manager_id_chip, IDs.SAVE_SPN_WEIGHTS_TO_FILE, member.id
    )
