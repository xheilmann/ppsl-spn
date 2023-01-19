import math
from src.network.exercise.util.manager_insert_in_share import (
    add_exercise_manager_insert_in_share,
)
from spn.structure.Base import Sum, get_nodes_by_type
from src.network.exercise.exercise_class import Exercise
from src.globals import IDs, Values


from functools import partial


def add_exercise_member_online(manager):
    all_members_online_exercise = Exercise(
        IDs.MEMBER_ONLINE,
        on_start=lambda x: None,
        # on_completion=partial(on_completion_member_online, manager),
    )
    manager.exercises.append(all_members_online_exercise)
    all_members_online_exercise.start()


def on_completion_member_online(manager, exercise):
    manager.default_on_completion(exercise)
    # from network.exercise.io.load_spn_from_file import load_spn_from_file

    # load_spn_from_file(manager)

    # for sum_node in get_nodes_by_type(manager.spn, Sum):
    #    for index in range(len(sum_node.children)):
    #        child_node = sum_node.children[index]
    #        data_id = f"({sum_node.id}, {child_node.id})"
    #        exact_weight = sum_node.weights[index]
    #        digits = int(math.log(Values.D_MULTIPLYER, 10) / 2)
    #        exact_weight_rounded = round(exact_weight, digits - 1)
    #        weight_to_insert = int(exact_weight_rounded * Values.D_MULTIPLYER)
    #        manager.data[data_id] = weight_to_insert
    #        print(
    #            f"For {data_id} we insert {exact_weight_rounded}*d from {exact_weight}"
    #        )
    #        add_exercise_manager_insert_in_share(manager, data_id)

    # from websockets.legacy.framing import Frame
