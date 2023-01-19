import pickle
import os.path
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


def add_exercise_train_structures_locally(manager, memberID):
    """
    exercise to train sum weights and leaf parameters on the local training dataset for each structure in the forest
    """
    manager.exercises.append(Exercise(IDs.TRAIN_STRUCTURES_LOCALLY, f"{memberID}"))


def train_structures_locally(member, message_value):
    components = message_value.split(";")
    single_member_id = components[0]
    if single_member_id == member.id:
        num_iterations = float(member.config[Keys.CONFIG_GENERAL_SECTION].get(
            Keys.CONFIG_GENERAL_NUM_LOCAL_ITERATIONS
        ))
        if num_iterations == 0.001:
            stopping_criteria = 0.001
            num_iterations = 200
            if int(member.config[Keys.CONFIG_GENERAL_SECTION].get(
            Keys.CONFIG_GENERAL_NUM_DIMS)) ==135:
                num_iterations = 90
        if num_iterations == 0.0001:
            stopping_criteria = 0.0001
            num_iterations = 200
            if int(member.config[Keys.CONFIG_GENERAL_SECTION].get(
            Keys.CONFIG_GENERAL_NUM_DIMS)) ==135:
                num_iterations = 90
        if num_iterations == 0.0005:
            stopping_criteria = 0.0005
            num_iterations = 200
            if int(member.config[Keys.CONFIG_GENERAL_SECTION].get(
            Keys.CONFIG_GENERAL_NUM_DIMS)) ==135:
                num_iterations = 90
        else:
            stopping_criteria = int(num_iterations)
            num_iterations = int(num_iterations +1)


        new_spns = member.config[Keys.CONFIG_GENERAL_SECTION].get(
            Keys.CONFIG_GENERAL_GENERATE_SPN_STRUCTURES
        )


        ckpt_filepath = member.config[f"ID_{member.id}"].get(
            Keys.CONFIG_CKPTS_FILE_PATH
        )
        if os.path.isfile(f"{ckpt_filepath}/0_ckp{stopping_criteria}.pickle") and new_spns not in ["true", "True"]: 
            #print("true")
            for spn_index in range(len(member.spn)):
                with open(fr"{ckpt_filepath}/{spn_index}_ckp{stopping_criteria}.pickle",
                          "rb") as f:
                    #print(fr"{ckpt_filepath}/{spn_index}_ckp{stopping_criteria}.pickle", os.path.isfile(fr"{ckpt_filepath}/{spn_index}_ckp{stopping_criteria}.pickle"))
                    member.spn[spn_index] = pickle.load(f)

                #print(f"{member.id}_{spn_index}:{member.spn[spn_index].weights}")
        #print(os.path.isfile(f"{ckpt_filepath}/0_ckp{num_iterations+10}.pickle" )   )        
        if os.path.isfile(f"{ckpt_filepath}/0_ckp{stopping_criteria+10}.pickle" ) and new_spns not in ["true", "True"]:
            #print("true")
            for spn_index in range(len(member.spn)):
                with open(fr"{ckpt_filepath}/{spn_index}_ckp{stopping_criteria+10}.pickle",
                          "rb") as f:
                    member.spn[spn_index] = pickle.load(f)

                #print(f"{member.id}_{spn_index}:{member.spn[spn_index].weights}")
            
        else: 
            #loading the training data in dtype float32
            private_data_file_path = member.config[f"ID_{member.id}"].get(
                Keys.CONFIG_PRIVATE_DATA_FILE_PATH
            )
            print(private_data_file_path)
            if private_data_file_path is not None:
                member.private_datadocker = np.array(
                    list(map(list, np.genfromtxt(private_data_file_path, dtype='float32')))
                )
            #loading evaluation data from file
            private_data_eval_file_path = member.config[f"ID_{member.id}"].get(
                Keys.CONFIG_PRIVATE_DATA_FOR_EVALUATION_FILE_PATH
            )
            if private_data_eval_file_path is not None:
                member.private_eval_datadocker = np.array(
                    list(map(list, np.genfromtxt(private_data_eval_file_path, dtype='float32')))
                )
            # training the structure locally
            #print(member.id)
            #print(member.private_datadocker)
            add_parametric_EM_support()
            for spn_index in range(len(member.spn)):
                spn = member.spn[spn_index]
                i = 0
                EM_optimization(spn, member.private_datadocker, 10)
                min_log_likl = np.mean(log_likelihood(spn, member.private_eval_datadocker))
                best_model = 0
                
                add_iterations = num_iterations
               
                with open(fr"{ckpt_filepath}/other/{spn_index}_ckp.pickle",
                                  "wb") as f:
                    pickle.dump(spn, f)
                while i < (num_iterations-10):
                    EM_optimization(spn, member.private_datadocker, 1)
                    log_likl = np.mean(log_likelihood(spn, member.private_eval_datadocker))
                    #print(log_likl)
                    if math.isinf(log_likl):
                        log_likl = np.mean(log_likelihood(spn, member.private_datadocker))

                    #print(np.mean(log_likelihood(spn, member.private_datadocker)))
                    
                            
                    if log_likl - min_log_likl > 0.001 and i < add_iterations+10 and stopping_criteria == 0.001:
                        
                        add_iterations_1 = i

                        #print("0.001",i, log_likl)
                        with open(fr"{ckpt_filepath}/{spn_index}_ckp{0.001}.pickle",
                                  "wb") as f:
                            pickle.dump(spn, f)
                    if log_likl - min_log_likl > 0.0005 and i < add_iterations+10 and stopping_criteria == 0.0005:
                        

                        add_iterations = i
                        #print(0.0005 ,i, log_likl)
                        with open(fr"{ckpt_filepath}/{spn_index}_ckp{0.0005}.pickle",
                                  "wb") as f:
                            pickle.dump(spn, f)
                    
                    if log_likl - min_log_likl > 0.0001 and i < add_iterations+10 and stopping_criteria == 0.0001:
                        

                        add_iterations = i
                        #print(0.0001 ,i, log_likl)
                        with open(fr"{ckpt_filepath}/{spn_index}_ckp{0.0001}.pickle",
                                  "wb") as f:
                            pickle.dump(spn, f)
                    
                    
                    if min_log_likl<log_likl:
                        best_model = i 
                        #print(best_model+10)
                        with open(fr"{ckpt_filepath}/other/{spn_index}_ckp.pickle",
                                  "wb") as f:
                            pickle.dump(spn, f)

                    if i+10 == 20: 
                        with open(fr"{ckpt_filepath}/other/{spn_index}_ckp.pickle",
                          "rb") as f:
                            spn1 = pickle.load(f)
                        with open(fr"{ckpt_filepath}/{spn_index}_ckp{i+10}.pickle",
                                  "wb") as f:
                            pickle.dump(spn1, f)
                    
                    if i+10 == 30: 
                          with open(fr"{ckpt_filepath}/other/{spn_index}_ckp.pickle",
                            "rb") as f:
                              spn1 = pickle.load(f)
                          with open(fr"{ckpt_filepath}/{spn_index}_ckp{i+10}.pickle",
                                    "wb") as f:
                              pickle.dump(spn1, f)
                  
                    if i+10 == 40: 
                          with open(fr"{ckpt_filepath}/other/{spn_index}_ckp.pickle",
                            "rb") as f:
                              spn1 = pickle.load(f)
                          with open(fr"{ckpt_filepath}/{spn_index}_ckp{i+10}.pickle",
                                    "wb") as f:
                              pickle.dump(spn1, f)
                   
                    if i+10 == 100: 
                          with open(fr"{ckpt_filepath}/other/{spn_index}_ckp.pickle",
                            "rb") as f:
                              spn1 = pickle.load(f)
                          with open(fr"{ckpt_filepath}/{spn_index}_ckp{i+10}.pickle",
                                    "wb") as f:
                              pickle.dump(spn1, f)
                    if i+10 == 300: 
                            with open(fr"{ckpt_filepath}/other/{spn_index}_ckp.pickle",
                              "rb") as f:
                                spn1 = pickle.load(f)
                            with open(fr"{ckpt_filepath}/{spn_index}_ckp{i+10}.pickle",
                                      "wb") as f:
                                pickle.dump(spn1, f)
                            
                    min_log_likl = max(log_likl, min_log_likl)
                    i += 1
                
               
                with open(fr"{ckpt_filepath}/{spn_index}_ckp{stopping_criteria}.pickle",
                              "rb") as f:
                    member.spn[spn_index] = pickle.load(f)
                    if member.config[Keys.CONFIG_GENERAL_SECTION].get(
                            Keys.CONFIG_GENERAL_PRIVATE
                    ) in ["False", "false"]:
                        spn_file_path = member.config[f"ID_{member.id}"].get(Keys.CONFIG_SPN_FILE_PATH)
                        with open(fr"{spn_file_path}/structure_{member.id}_{spn_index}",
                                  "wb") as f:
                            pickle.dump(member.spn[spn_index], f)

                        #print(f"{member.id}_{spn_index}:{member.spn[spn_index].weights}")

    
    member.network_socket.send(
        member.manager_id_chip, IDs.TRAIN_STRUCTURES_LOCALLY, member.id)
