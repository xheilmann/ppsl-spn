from src.network.exercise.exercise_class import Exercise
from src.globals import IDs


def add_exercise_delete_data_at_ids(manager, *data_ids_to_delete):
    # print(f"message ids to delete before tuple: {data_ids_to_delete}")
    if isinstance(data_ids_to_delete[0], list):
        data_ids_to_delete = data_ids_to_delete[0]
    # print(f"message ids to delete: {data_ids_to_delete}")
    if isinstance(data_ids_to_delete, str):
        ids_to_delete = data_ids_to_delete
    else:
        ids_to_delete = ";".join(data_ids_to_delete)
    # print(f"message ids to delete after join: {ids_to_delete}")
    # ids_to_delete = ";".join(data_ids_to_delete)
    manager.exercises.append(
        Exercise(
            IDs.DELETE_DATA_AT_ID,
            ids_to_delete,
        )
    )


def delete_data_at_id(member, message_value):
    # print(f"data ids to delete {message_value}")
    data_ids_to_delete = message_value.split(";")
    # print(f"data ids to delete after split {data_ids_to_delete}")
    for data_id_to_delete in data_ids_to_delete:
        del member.data[data_id_to_delete]
    member.network_socket.send(member.manager_id_chip, IDs.DELETE_DATA_AT_ID, member.id)
