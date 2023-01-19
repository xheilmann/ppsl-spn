import numpy as np
from spn.structure.Base import Sum, get_nodes_by_type, Product
from spn.algorithms.Inference import likelihood
from src.spn.Local_Inference import likelihood as local_likelihood
from src.evaluation import Evaluation
from src.network.exercise.exercise_class import Exercise
from src.globals import IDs, Keys
from spn.structure.Base import eval_spn_bottom_up
import pickle

def add_exercise_insert_edge_usage(manager):
    """
    exercise to insert the positive contributions a child maes to its parent sum node
    """
    manager.exercises.append(Exercise(IDs.INSERT_EDGE_USAGE))


def insert_edge_usage(member, message_value):

    for structure_id in range(len(member.spn)):
        
        spn = member.spn[structure_id]
        likl, results = (local_likelihood(spn, member.private_data))
        member.find_maximum = []
        member.count_times = {}
        counter = 0
        for child in spn.children:
                # data_id = f"ProductNode_{j+1}"
            member.find_maximum.append(results.get(child)*spn.weights[counter])
            member.count_times[f"({spn.id}, {child.id})"] = 0
            counter+=1
        counter = 0
        for t in range(len(member.find_maximum[0])):
            max = 0
            for i in range(len(member.find_maximum)):
                temp = member.find_maximum[i][t]
                if max < temp:
                    counter = i
                    max = temp
                
            member.count_times[f"({spn.id}, {counter+1})"] = member.count_times.get(f"({spn.id}, {counter+1})") + 1
        if member.config[Keys.CONFIG_GENERAL_SECTION].get(
                Keys.CONFIG_GENERAL_PRIVATE
        ) in ["False", "false"]:
            spn_file_path = member.config[f"ID_{member.id}"].get(Keys.CONFIG_SPN_FILE_PATH)
            with open(fr"{spn_file_path}/edge_usage_{member.id}_{structure_id}",
                      "wb") as f:
                pickle.dump(member.count_times, f)
        else:
            for data_id, value in member.count_times.items():
                #print(f"id {member.id} for {data_id} we got value {value}")
                member.insert_in_share(f"{structure_id}_{data_id}", value)
    
        


    member.network_socket.send(member.manager_id_chip, IDs.INSERT_EDGE_USAGE, member.id)





