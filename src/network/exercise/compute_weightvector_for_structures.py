import numpy as np
import csv
import math
from spn.algorithms.Inference import likelihood, log_likelihood
from spn.structure.leaves.parametric.EM import add_parametric_EM_support

from src.network.exercise.exercise_class import Exercise
from src.globals import IDs, Keys

from spn.structure.Base import get_nodes_by_type
from spn.structure.Base import Sum
from spn.algorithms.EM import EM_optimization
import pickle

def add_exercise_compute_weightvector_for_structures(manager):
    """
    weights the structures on the local dataset
    """
    manager.exercises.append(Exercise(IDs.COMPUTE_WEIGHTVECTOR_FOR_STRUCTURES))


        
def compute_weightvector_for_structures(member, message_value):
    # loading validation data
    private_data_for_evaluation_file_path = member.config[f"ID_{member.id}"].get(
        Keys.CONFIG_PRIVATE_DATA_FOR_EVALUATION_FILE_PATH
    )

    if private_data_for_evaluation_file_path is not None:
        member.private_datadocker_for_evaluation = np.array(
            list(map(list, np.genfromtxt(private_data_for_evaluation_file_path, dtype='float32')))
        )
    
   
    member.all_weights = []
    for structure in member.spn:
        member.loglikl = log_likelihood(structure, member.private_datadocker_for_evaluation)
        
        member.loglikl = np.sum(member.loglikl)/len(member.loglikl)
        if math.isinf(member.loglikl):
            member.loglikl = np.mean(log_likelihood(structure, member.private_datadocker))
        member.loglikl = (1/abs(member.loglikl))

        member.all_weights.append (member.loglikl)

    member.loglikl_structure_weights = [j/sum(member.all_weights) for j in member.all_weights]
    #print (member.loglikl_structure_weights)

    member.all_weights = []
    for structure in member.spn:
        member.loglikl = log_likelihood(structure, member.private_datadocker_for_evaluation)
        
        member.loglikl = np.sum(member.loglikl) / len(member.loglikl)
        if math.isinf(member.loglikl):
            member.loglikl = np.mean(log_likelihood(structure, member.private_datadocker))
        member.loglikl = (1 / (member.loglikl**2))

        member.all_weights.append(member.loglikl)

    member.enf_loglikl_structure_weights = [j / sum(member.all_weights) for j in member.all_weights]
    #print(member.enf_loglikl_structure_weights)

    #member.all_weights = []
    #for structure in member.spn:
        #member.likl = likelihood(structure, member.private_datadocker_for_evaluation)
        #member.likl = np.sum(member.likl)/len(member.likl)

        #member.all_weights.append(member.likl)

    member.likl_structure_weights = [j / sum(member.all_weights) for j in member.all_weights]
    #print(member.likl_structure_weights)

    member.all_weights = []
    for structure in member.spn:
        member.loglikl = log_likelihood(structure, member.private_datadocker_for_evaluation)
        
        member.loglikl = np.sum(member.loglikl) / len(member.loglikl)
        if math.isinf(member.loglikl):
            member.loglikl = np.mean(log_likelihood(structure, member.private_datadocker))
        member.loglikl = (1 / abs(member.loglikl))

        member.all_weights.append(member.loglikl)

    all_weights_sorted = sorted(member.all_weights)
    member.ranking_structure_weights = [(all_weights_sorted.index(entry)+1) for entry in member.all_weights]
    member.ranking_structure_weights = [j / sum(member.ranking_structure_weights) for j in member.ranking_structure_weights]
    #print(member.ranking_structure_weights)
    
    
    if member.config[Keys.CONFIG_GENERAL_SECTION].get(
            Keys.CONFIG_GENERAL_PRIVATE
    ) in ["False", "false"]:
        spn_file_path = member.config[f"ID_{member.id}"].get(Keys.CONFIG_SPN_FILE_PATH)
        with open(fr"{spn_file_path}/weights_{member.id}",
                  "wb") as f:
            pickle.dump(member.ranking_structure_weights, f)
    else:
    #share weight vector
        for j in range(0, len(member.ranking_structure_weights)):
            value = int((member.ranking_structure_weights[j]/len(member.id_chips_for_id)) * member.d_multiplyer)
            data_id = f"ranking_weight_{j}"
            #member.data[data_id] = value
            #print(f"id {member.id} for {data_id} we got value {value}")
            member.insert_in_share(data_id, value)
        
        for j in range(0, len(member.loglikl_structure_weights)):
            value = int((member.loglikl_structure_weights[j]/len(member.id_chips_for_id)) * member.d_multiplyer)
            data_id = f"loglikl_weight_{j}"
            #member.data[data_id] = value
            #print(f"id {member.id} for {data_id} we got value {value}")
            member.insert_in_share(data_id, value)
        
        #for j in range(0, len(member.likl_structure_weights)):
            #value = int((member.likl_structure_weights[j]/len(member.id_chips_for_id)) * member.d_multiplyer)
            #data_id = f"likl_weight_{j}"
            #print(f"id {member.id} for {data_id} we got value {value}")
            #member.insert_in_share(data_id, value)
            
        for j in range(0, len(member.enf_loglikl_structure_weights)):
            value = int((member.enf_loglikl_structure_weights[j]/len(member.id_chips_for_id)) * member.d_multiplyer)
            data_id = f"enf_loglikl_weight_{j}"
            #member.data[data_id] = value
            #print(f"id {member.id} for {data_id} we got value {value}")
            member.insert_in_share(data_id, value)

    member.network_socket.send(
        member.manager_id_chip, IDs.COMPUTE_WEIGHTVECTOR_FOR_STRUCTURES, member.id)
