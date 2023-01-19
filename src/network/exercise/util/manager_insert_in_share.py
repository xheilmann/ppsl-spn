from src.network.exercise.exercise_class import Exercise
from src.globals import IDs

from functools import partial
import logging

logger = logging.getLogger(__name__)


def add_exercise_manager_insert_in_share(manager, data_id):
    """
    share a number saved under data_id with the other members in the network
    """
    manager.exercises.append(
        Exercise(
            IDs.MANAGER_INSERT_IN_SHARE,
            f"{data_id}",
            on_start=partial(on_start_manager_insert_in_share, manager),
        )
    )


from datetime import datetime
from src.mathy.polynomial import polynom_for_secret


def on_start_manager_insert_in_share(manager, exercise):
    # print(f"sta: on_start_manager_insert: {datetime.now()}")
    data_id = exercise.value
    value = manager.data.get(data_id)
    # new_value = f"{data_id};{manager.data.get(data_id)}"
    # exercise.value = new_value
    ##manager.insert_in_share(data_id, manager.data.get(data_id), with_id_appendix=False)

    poly = polynom_for_secret(
        manager.max_degree_for_polynomials, manager.prim_number, value
    )
    logger.info_spn(
        f'{datetime.now()}: Exercise "{exercise.id}" is send to all members'
    )
    for id_chip in manager.id_chips_for_id.values():
        share_value = poly(id_chip.id).item()

        manager.network_socket.send(id_chip, exercise.id, f"{data_id};{share_value}")

    # new_value = f"{data_id};{manager.data.get(data_id)}"
    # exercise.value = new_value
    # print(f"aft: on_start_manager_insert: {datetime.now()}")
    ##manager.default_on_start(exercise)
    # print(f"end: on_start_manager_insert: {datetime.now()}")
    # del self.data[data_id]


def manager_insert_in_share(member, message_value):
    components = message_value.split(";")  ##
    data_id = components[0]  ##
    value = int(components[1])  ##
    member.data[data_id] = value  ##

    member.network_socket.send(
        member.manager_id_chip, IDs.MANAGER_INSERT_IN_SHARE, member.id
    )
