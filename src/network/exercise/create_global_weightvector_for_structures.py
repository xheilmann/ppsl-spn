from src.network import manager
from src.network.exercise.exercise_class import Exercise
from src.globals import IDs
from src.network.exercise.reveal.reveal_number import add_exercise_reveal_number


#TODO Rückgängig auf einen vector machen 

def add_exercise_create_global_weightvector_for_structures(manager):
    """
    creates the global weight vector of the structures on which all clients hold a share
    """
    manager.exercises.append(Exercise(IDs.CREATE_GLOBAL_WEIGHTVECTOR_FOR_STRUCTURES))

def create_global_weightvector_for_structures(member, message_value):
    # combining the shared structure weightvectors to a single shared one
    for j in range(0, len(member.spn)):
        data_id = f"ranking_weight_{j}"
        member.data[data_id] = 0
        for member_id in member.id_chips_for_id.keys():
            member.addTo(data_id, f"{data_id}_{member_id}")
            del member.data[f"{data_id}_{member_id}"]
    
    for j in range(0, len(member.spn)):
        data_id = f"loglikl_weight_{j}"
        member.data[data_id] = 0
        for member_id in member.id_chips_for_id.keys():
            member.addTo(data_id, f"{data_id}_{member_id}")
            del member.data[f"{data_id}_{member_id}"]

    for j in range(0, len(member.spn)):
        data_id = f"enf_loglikl_weight_{j}"
        member.data[data_id] = 0
        for member_id in member.id_chips_for_id.keys():
            member.addTo(data_id, f"{data_id}_{member_id}")
            del member.data[f"{data_id}_{member_id}"]

    member.network_socket.send(
        member.manager_id_chip, IDs.CREATE_GLOBAL_WEIGHTVECTOR_FOR_STRUCTURES, member.id)