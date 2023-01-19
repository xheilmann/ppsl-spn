import os

from src.network.exercise.io.save_spn_weights_to_file import (
    add_exercise_save_spn_weights_to_file,
)
from spn.algorithms.layerwise.layers import Sum
from src.network.exercise.exercise_class import Exercise
from src.globals import IDs, Keys

from spn.structure.Base import get_nodes_by_type, get_topological_order_layers

from functools import partial
import pickle



def add_exercise_load_spn_from_file(manager):
    """
    loads SPNs from the manager
    """
    manager.exercises.append(
        Exercise(
            IDs.LOAD_SPN_FROM_FILE,
            on_completion=partial(on_completion_load_spn_from_file, manager),
        )
    )



def on_completion_load_spn_from_file(manager, exercise):
    manager.default_on_completion(exercise)
    # from spn.io.Graphics import plot_spn
    # plot_spn(manager.spn, "plots/paper_spn_2.png")
    # add_exercise_save_spn_weights_to_file(manager)
    from spn.algorithms.Statistics import get_structure_stats
    for i in range(len(manager.spn)):
        print(f"Structure_number:{i}")
        print(get_structure_stats(manager.spn[i]))



def load_spn_from_file(member, message_value=None):
    member.spn = []
    member.layers = []
    spn_file_path = member.config[f"ID_{member.id}"].get(Keys.CONFIG_SPN_FILE_PATH)
    assert (
        spn_file_path is not None
    ), f'No "{Keys.CONFIG_SPN_FILE_PATH}" given in the config file'
    ls = sorted(os.listdir(spn_file_path))
    for file in ls:
        with open(spn_file_path+"/"+file,"rb") as f:
            spn = pickle.load(f)
        member.spn.append(spn)
        member.layers.append(get_topological_order_layers(spn))

    member.network_socket.send(
        member.manager_id_chip, IDs.LOAD_SPN_FROM_FILE, member.id
    )