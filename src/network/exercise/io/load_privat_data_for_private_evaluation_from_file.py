from src.network.exercise.exercise_class import Exercise
from src.globals import IDs, Keys
import numpy as np


def add_exercise_load_private_data_for_private_evaluation_from_file(manager):
    manager.exercises.append(
        Exercise(IDs.LOAD_PRIVATE_DATA_FOR_PRIVATE_EVALUATION_FROM_FILE)
    )


def load_private_data_for_private_evaluation_from_file(member, message_value=None):
    private_data_for_evaluation_file_path = member.config[f"ID_{member.id}"].get(
        Keys.CONFIG_PRIVATE_DATA_FOR_EVALUATION_FILE_PATH
    )

    if private_data_for_evaluation_file_path is not None:

        private_inputs_for_leafes = np.array(
            list(
                map(
                    list,
                    np.genfromtxt(private_data_for_evaluation_file_path, dtype=None),
                )
            )
        )

        # private_input_for_leafes = np.array([private_input_for_leafes_current_line])

        member.private_data_for_evaluation = private_inputs_for_leafes
    else:
        member.private_data_for_evaluation = np.array([])  # TODO: test it!

    member.network_socket.send(
        member.manager_id_chip,
        IDs.LOAD_PRIVATE_DATA_FOR_PRIVATE_EVALUATION_FROM_FILE,
        member.id,
    )
