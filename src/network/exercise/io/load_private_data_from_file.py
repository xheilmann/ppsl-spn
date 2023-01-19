from src.network.exercise.exercise_class import Exercise
from src.globals import IDs, Keys
import numpy as np


def add_exercise_load_private_data_from_file(manager):
    manager.exercises.append(Exercise(IDs.LOAD_PRIVATE_DATA_FROM_FILE))


def load_private_data_from_file(member, message_value=None):
    private_data_file_path = member.config[f"ID_{member.id}"].get(
        Keys.CONFIG_PRIVATE_DATA_FILE_PATH
    )
    if private_data_file_path is not None:
        member.private_data = np.array(
            list(map(list, np.genfromtxt(private_data_file_path, dtype=None)))
        )
    else:
        member.private_data = np.array([])  # TODO: test it!

    member.network_socket.send(
        member.manager_id_chip, IDs.LOAD_PRIVATE_DATA_FROM_FILE, member.id
    )
