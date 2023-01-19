from src.network.exercise.exercise_class import Exercise
from src.globals import IDs, Keys

def add_exercise_load_spn_weights_from_file(manager, structure_id):
    """
    Optional method to load parameters from a file, e.g. for inference
    """
    manager.exercises.append(Exercise(IDs.LOAD_SPN_WEIGHTS_FROM_FILE, structure_id))


def load_spn_weights_from_file(member, message_value):
    structure_id = message_value
    spn_weights_file_path = member.config[f"ID_{member.id}"].get(
        Keys.CONFIG_SPN_WEIGHTS_FILE_PATH
    )
    f = open(spn_weights_file_path + f"/structure_{structure_id}", "r")
    for line in f.read().splitlines():
        data_id, value_str = line.split("=")
        value = int(value_str)

        member.data[data_id] = value
    f.close()
    member.network_socket.send(
        member.manager_id_chip, IDs.LOAD_SPN_WEIGHTS_FROM_FILE, member.id
    )
