from spn.algorithms.Inference import log_likelihood

import numpy as np
from spn.structure.Base import Sum, Product, get_nodes_by_type, Leaf

from src.network.exercise.exercise_class import Exercise
from src.globals import IDs, Keys
import os
from collections import Counter
import pickle


def add_exercise_do_fl_step(manager):
    """
    generates the initial RAT-SPN forest based on the RAT-SPN dictionary input
    """
    
    manager.exercises.append(Exercise(IDs.FL_STEP))


def fl_step(member, message_value):
    if member.id =="1":
        spn_file_path = member.config[f"ID_{member.id}"].get(Keys.CONFIG_SPN_FILE_PATH)
        assert (
                spn_file_path is not None
        ), f'No "{Keys.CONFIG_SPN_FILE_PATH}" given in the config file'
        weights=[0 for j in range(len(member.spn))]
        global_likl=[]
        
        combined_eval_data =member.config[f"ID_{member.id}"].get(
            Keys.CONFIG_GLOBAL_DATA_FOR_EVALUATION_FILE_PATH
        )
    
        if combined_eval_data is not None:
            member.eval_data = np.array(
                list(map(list, np.genfromtxt(combined_eval_data, dtype='float32')))
            )
        for structure_id in range(len(member.spn)):
            spns=[]
            edge_usage =Counter({})
            
            for member_id in range(1,len(member.id_chips_for_id)+1):
                    file = f"structure_{member_id}_{structure_id}"
                    with open(spn_file_path + "/" + file, "rb") as f:
                        spn = pickle.load(f)
                    spns.append(get_nodes_by_type(spn, ntype=Leaf))
                    file2= f"edge_usage_{member_id}_{structure_id}"
                    with open(spn_file_path + "/" + file2, "rb") as f:
                        temp = Counter(pickle.load(f))
                        print(temp)
                        edge_usage = edge_usage + temp
                        
                    
            
            
            leaves = get_nodes_by_type(member.spn[structure_id], ntype=Leaf)
            all_edge_usages = sum(edge_usage.values())
            for i in range(len(spns[0])):
                p = (np.mean([spns[j][i].p for j in range(len(spns))]))
                leaves[i].p = p
                print(f"{structure_id}_leaf{i}= {p}")
            for child in range(len(member.spn[structure_id].children)):
                #print(edge_usage)
                if edge_usage.get(f"(0, {child+1})") != None:
                    member.spn[structure_id].weights[child] = edge_usage.get(f"(0, {child+1})")/all_edge_usages
                else: 
                    member.spn[structure_id].weights[child]=0
                print(f"{structure_id}_sum_weight{child}={member.spn[structure_id].weights[child]}")
    
            loglikl = log_likelihood(member.spn[structure_id],member.eval_data)
            mean = np.sum(loglikl) / len(loglikl)
            print(mean)
            global_likl.append(mean)
        
        for member_id in range(1,len(member.id_chips_for_id)+1):
            file3=f"weights_{member_id}"
            with open(spn_file_path + "/" + file3, "rb") as f:
                temp = pickle.load(f)
                weights= [weights[j]+temp[j] for j in range(len(temp))]
        weights= [weights[j]/len(member.id_chips_for_id) for j in range(len(weights))]
        print(f"structure_weights={weights}")
        ranking_overall_loglikl = np.sum([global_likl[j] * weights[j] for j in range(0, len(global_likl))])
        print(f"ranking_overall-Log_likelihood={ranking_overall_loglikl} ")

        dir = spn_file_path
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
 
    member.network_socket.send(
        member.manager_id_chip,
        IDs.FL_STEP,
        member.id,
    )