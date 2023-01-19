import logging

logger = logging.getLogger(__name__)
from datetime import datetime
from tqdm import tqdm


class Exercise:
    # current_exercise_number = 0

    amount_members = 0

    def __init__(self, id, value=None, on_start=None, on_completion=None) -> None:
        self.id = id
        self.completed_member_ids = []

        self.is_running = False
        self.is_finished = False

        if value is not None:
            self.value = value
        else:
            self.value = ""

        if on_completion is not None:
            self.on_completion = on_completion

        if on_start is not None:
            self.on_start = on_start

    def set_value(self, value):
        self.value = value

    def start(self):
        self.is_running = True
        self.on_start(self)

    def add_id_of_completed_member(self, member_id):
        self.completed_member_ids.append(member_id)
        if len(self.completed_member_ids) == self.amount_members:
            self.on_completion(self)
            self.is_running = False
            self.is_finished = True
