import numpy as np
import csv


from spn.algorithms.Inference import likelihood, log_likelihood
from spn.structure.leaves.parametric.EM import add_parametric_EM_support

from src.network.exercise.exercise_class import Exercise
from src.globals import IDs, Keys

from spn.structure.Base import get_nodes_by_type, Leaf
from spn.structure.Base import Sum
from spn.algorithms.EM import EM_optimization
from src.spn.Local_Inference import likelihood as local_likelihood


def add_exercise_measure_performance(manager):
    manager.exercises.append(Exercise(IDs.MEASURE_PERFORMANCE))


def measure_performance(member, message_value):
    """
    measures the performance of the RAT-SPN forest's different weighting methods an writes them to ../resources/output/weighting_methods.out

    :param member: member in the network

    """
    if member.id == "1":
        
        global_likl = []
        combined_eval_data = member.config[f"ID_{member.id}"].get(
            Keys.CONFIG_GLOBAL_DATA_FOR_EVALUATION_FILE_PATH
        )
        output_path = member.config[Keys.CONFIG_GENERAL_SECTION].get(
            Keys.CONFIG_GENERAL_OUTPUT_FILE_PATH
        )

        if combined_eval_data is not None:
            
            member.eval_data = np.array(
                list(map(list, np.genfromtxt(combined_eval_data, dtype='float32')))
            )
        loglikl_weight_vector = []
        ranking_weight_vector = []
        likl_weight_vector = []
        enf_loglikl_weight_vector = []
        for j in range(0, len(member.spn)):
            data_id = f"ranking_weight_{j}"
            ranking_weight_vector.append(member.data.get(data_id)/member.d_multiplyer)
            data_id = f"loglikl_weight_{j}"
            loglikl_weight_vector.append(member.data.get(data_id)/member.d_multiplyer)
            #data_id = f"likl_weight_{j}"
            #likl_weight_vector.append(member.data.get(data_id)/member.d_multiplyer)
            data_id = f"enf_loglikl_weight_{j}"
            enf_loglikl_weight_vector.append(member.data.get(data_id)/member.d_multiplyer)
            
            saving_id_loglikl = f"{j}_loglikelihood"
            spn = member.spn[j]
            for sum in get_nodes_by_type(spn, ntype=Sum):
                if sum.id == 0: 
                    sum.weights = []
                    for child in sum.children:    
                        data_id = f"{j}_({sum.id}, {child.id})"
                        if child == sum.children[-1]:
                            sum.weights.append(1-np.sum(sum.weights))
                        else:
                            sum.weights.append(member.data.get(data_id)/member.d_multiplyer)

                else: 
                    sum.weights = [1 / len(sum.weights) for j in range(len(sum.weights))]
            for leaf in get_nodes_by_type(spn, ntype=Leaf):
                data_id_p = f"{j}_({leaf.id}, {leaf.id})_p"
                leaf.p = member.data.get(data_id_p)/member.d_multiplyer
            loglikl = log_likelihood(spn, member.eval_data)
            likl = likelihood(spn, member.eval_data)
            mean = np.sum(loglikl)/len(loglikl)
            mean1 = np.sum(likl)/len(likl)
            print(mean, mean1)
            member.data[saving_id_loglikl] = mean

            
            member.network_socket.send(member.manager_id_chip, saving_id_loglikl, mean)
            global_likl.append(mean)
        saving_id_overall_loglikl = "overall_loglikelihood"
        loglikl_overall_loglikl = np.sum([global_likl[j] * loglikl_weight_vector[j] for j in range(0, len(global_likl))])
        enf_loglikl_overall_loglikl = np.sum([global_likl[j] * enf_loglikl_weight_vector[j] for j in range(0, len(global_likl))])
        #likl_overall_loglikl = np.sum([global_likl[j] * likl_weight_vector[j] for j in range(0, len(global_likl))])
        ranking_overall_loglikl = np.sum([global_likl[j] * ranking_weight_vector[j] for j in range(0, len(global_likl))])
        with open(output_path, "a") as out_file:
            out_file.write(f"loglikelihood_method: {loglikl_overall_loglikl}\n")
            out_file.write(f"enforced_loglikelihood_method: {enf_loglikl_overall_loglikl}\n")
            out_file.write(f"ranking_method: {ranking_overall_loglikl}\n")


        #member.network_socket.send(member.manager_id_chip, saving_id_overall_loglikl, overall_loglikl)
    
       
                
    member.network_socket.send(
        member.manager_id_chip, IDs.MEASURE_PERFORMANCE, member.id)
