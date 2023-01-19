import time
from src.network.exercise.exercise_class import Exercise
from src.globals import IDs
from functools import partial
import logging

logger = logging.getLogger(__name__)


def add_exercise_dummy(manager, data_id="dumm exercise"):
    """
    exercise for statistics on exercises used during a whole protocol
    """
    manager.exercises.append(
        Exercise(
            IDs.DUMMY, data_id, on_completion=partial(on_completion_dummy, manager)
        )
    )


def on_completion_dummy(manager, exercise):
    manager.default_on_completion(exercise)
    from src.websockets.legacy.framing import Frame
    import pandas

    sum_of_time = 0
    names = [
        "Exercise ID",
        "counter",
        "total time",
        "time per execution",
        "percantage of total time",
    ]
    rows = []
    for id, measurement_stored in manager.exercise_measuring.items():
        counter, time_stored = measurement_stored
        sum_of_time += time_stored
        # print(
        #    f"{id}:\tcounter: {counter}\ttime: {time_stored}\ttime per call: {time_stored/counter}"
        # )
        rows.append([id, counter, time_stored, (time_stored / counter)])

    rows_with_percentage_of_time = list(
        map(lambda row: row + [round(((row[-2]) / sum_of_time) * 100)], rows)
    )

    data_frame = pandas.DataFrame(rows_with_percentage_of_time, columns=names)
    logger.info_spn(f"\n{data_frame.to_string()}")
    
    # with open(f"/ppspn_env/resources/output/evaluation_{single_member_id}.out", "a") as out_file:
    #        out_file.write(f"{member.data.get(data_id_to_save)}\n")

    logger.info_spn(f"frame counter: {Frame.MEASUREMENT_total_message_amount}")
    logger.info_spn(f"frame length counter: {Frame.MEASUREMENT_total_message_lengths}")
    logger.info_spn(f"total time: {sum_of_time}")


def dummy(member, message_value):
    data_id = message_value
    print(f"{data_id}:\tid: {member.id} data: {member.data}")
    member.network_socket.send(member.manager_id_chip, IDs.DUMMY, member.id)
    # from websockets.legacy.framing import Frame
    # print(f"frame counter: {Frame.MEASUREMENT_total_message_amount}")
    # print(f"frame length counter: {Frame.MEASUREMENT_total_message_lengths}")
