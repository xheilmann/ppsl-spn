import math
from spn.algorithms.Inference import likelihood, log_likelihood
from spn.structure.Base import Leaf, get_nodes_by_type

from src.network import manager
from src.network.exercise.exercise_class import Exercise
from src.globals import IDs, Keys, Values
from src.network.exercise.math.multiplication import add_exercise_multiplication
from src.network.exercise.util.dummy import add_exercise_dummy
from src.network.exercise.evaluation.evaluate_spn_bottom_up import (
    add_exercise_evaluate_spn_bottom_up,
)

import numpy as np

#unused function for a test
def add_exercise_fast_evaluation(
        manager, member_id, line_index_of_input_for_private_evaluation
):
    for i in range(len(manager.spn)):
        structure_id = i
        manager.exercises.append(
            Exercise(
                IDs.EVALUATION_SINGLE_MEMBER_LEAF_STEP,
                f"{member_id};{line_index_of_input_for_private_evaluation};{structure_id}",
            )
        )

        add_exercise_evaluate_spn_bottom_up(manager, structure_id)
        manager.exercises.append(
            Exercise(IDs.EVALUATION_SEND_TO_SINGLE_MEMBER_STEP, f"{member_id};{structure_id}")
        )
    manager.exercises.append(
        Exercise(
            IDs.EVALUATION_SINGLE_MEMBER_JOIN_STEP,
            f"{member_id};{line_index_of_input_for_private_evaluation}",
        )
    )


def evaluation_single_member_leaf_step(member, message_value):
    components = message_value.split(";")
    single_member_id = components[0]
    line_index_of_input_for_private_evaluation = int(components[1])
    structure_id = int(components[2])

    if single_member_id == member.id:
        print(member.data)
        private_data_for_evaluation_file_path = member.config[f"ID_{member.id}"].get(
            Keys.CONFIG_PRIVATE_DATA_FOR_EVALUATION_FILE_PATH
        )

        if private_data_for_evaluation_file_path is not None:
            member.private_datadocker_for_evaluation = np.array(
                list(map(list, np.genfromtxt(private_data_for_evaluation_file_path, dtype=None)))
            )

        leaf_nodes = get_nodes_by_type(member.spn[structure_id], Leaf)
        private_inputs_for_leafes = member.private_datadocker_for_evaluation

        private_input_for_leafes_current_line = private_inputs_for_leafes[
            line_index_of_input_for_private_evaluation
        ]

        private_input_for_leafes = np.array([private_input_for_leafes_current_line]).reshape(-1,
                                                                                             len(private_input_for_leafes_current_line))

        for index in range(len(leaf_nodes)):
            leaf_node = leaf_nodes[index]
            # private_input_for_leaf = np.array([[private_input_for_leafes[index]]])

            data_id_leaf_node = f"{structure_id}_({leaf_node.id}, {leaf_node.id})_result"
            exact_result = likelihood(leaf_node, private_input_for_leafes)
            # print("exact result {}".format(exact_result[0]))
            assert not np.any(np.isnan(exact_result[0][0])), "ll is nan %s " % index
            if np.isinf(exact_result[0][0]):
                exact_result[0][0] = 1
            digits = int(math.log(member.d_multiplyer, 2) / 2)
            exact_result_rounded = round(abs(exact_result[0][0]), digits - 1)
            # print(exact_result_rounded, exact_result)
            result_value_for_leaf = math.floor(
                exact_result_rounded * (member.d_multiplyer)
            ) % member.prim_number

            print(data_id_leaf_node, result_value_for_leaf, exact_result_rounded * member.d_multiplyer,
                  (exact_result[0][0]))
            member.insert_in_share(
                data_id_leaf_node, result_value_for_leaf, with_id_appendix=False
            )

    member.network_socket.send(
        member.manager_id_chip,
        IDs.EVALUATION_SINGLE_MEMBER_LEAF_STEP,
        member.id,
    )


def evaluation_send_to_single_member_step(member, message_value):
    components = message_value.split(";")
    single_member_id = components[0]
    structure_id = int(components[1])

    single_member_id_chip = member.id_chips_for_id.get(single_member_id)
    data_id_result = f"{structure_id}_(0, 0)_result"
    value = member.data.get(data_id_result)

    member.network_socket.send(
        single_member_id_chip, f"{data_id_result}_{member.id}", value
    )
    member.network_socket.send(
        member.manager_id_chip,
        IDs.EVALUATION_SEND_TO_SINGLE_MEMBER_STEP,
        member.id,
    )


def evaluation_single_member_join_step(member, message_value):
    components = message_value.split(";")
    single_member_id = components[0]
    line_index_of_input_for_private_evaluation = int(components[1])
    # structure_id = int(components[2])
    data_id_to_save = f"eval_{line_index_of_input_for_private_evaluation}_result"
    member.data[data_id_to_save] = 0
    for i in range(len(member.spn)):
        if single_member_id == member.id:
            data_id_result = f"{i}_(0, 0)_result"
            member.join_polynomial_shares(data_id_result)
            print(
                f"For member {single_member_id} the {data_id_result}_for_{line_index_of_input_for_private_evaluation} is {member.data.get(data_id_result)}"
            )
            member.data[data_id_to_save] = (member.data[data_id_to_save] + member.data.get(data_id_result))

    member.data[data_id_to_save] = member.data[data_id_to_save] / (member.d_multiplyer ** 3)
    with open(f"../resources/output/{single_member_id}/structure_0.out", "a") as out_file:
        result = (member.data.get(data_id_to_save))
        out_file.write(f"{result}\n")
    print(
        f"For member {single_member_id} the {data_id_to_save} is {member.data.get(data_id_to_save)}"
    )
    member.network_socket.send(
        member.manager_id_chip,
        IDs.EVALUATION_SINGLE_MEMBER_JOIN_STEP,
        member.id,
    )
