import math
from operator import sub
from numpy.lib.function_base import copy

from spn.algorithms.Inference import likelihood
from decimal import Decimal
from decimal import getcontext
from src.globals import (
    IDs,
    Keys,
    Values,
)

from random import randint


from src.network.id_chip import IDChip
from src.network.network_socket import NetworkSocket
from spn.structure.Base import Leaf, Node, Sum, get_nodes_by_type
import configparser

import logging
from decimal import *
from datetime import datetime

logger = logging.getLogger(__name__)

import nest_asyncio

nest_asyncio.apply()
# __import__("IPython").embed()

from spn.structure.Base import assign_ids, rebuild_scopes_bottom_up

from src.mathy.polynomial import polynom_for_secret
from src.evaluation import Evaluation
import numpy as np
import time

import threading

# from galois import Poly


class Member:
    """Base Class for all roles in the SPN computing network"""

    def __init__(self, configuration_filepath, id):
        self.__data = {}
        self.__id = id
        self.table_time = 0
        self.load_config(configuration_filepath)
        self.__d_multiplyer_inverse = pow(
            int(self.d_multiplyer), self.prim_number - 2, self.prim_number
        )

        self.build_id_chips_for_id()
        self.build_exercise_hooks()
        self.compute_recombination_vector()
        self.network_socket = NetworkSocket(self)

    @property
    def config(self):
        return self.__config

    @property
    def id(self):
        return self.__id

    @property
    def id_chip(self):
        return self.__id_chip

    @property
    def data(self):
        return self.__data

    @property
    def max_degree_for_polynomials(self):
        return (
            len(self.id_chips_for_id.values()) // 2
        )  # - 1  # TODO: has it to be less than a half or is half possible too?

    @property
    def prim_number(self):
        return self.__prim_number

    @property
    def recombination_vector(self):
        return self.__recombination_vector

    @property
    def joint_random_zero_minimum(self):
        return self.__joint_random_zero_minimum

    @property
    def d_multiplyer(self):
        return self.__d_multiplyer

    @property
    def d_multiplyer_inverse(self):
        return self.__d_multiplyer_inverse

    @property
    def truncate_n(self):
        return self.__truncate_n

    @property
    def truncate_t(self):
        return self.__truncate_t

    @property
    def sharing_over_integer_max_secret(self):
        return self.__sharing_over_integer_max_secret

    @property
    def sharing_over_integer_allowed_bit_length_of_secret(self):
        return self.__sharing_over_integer_allowed_bit_length_of_secret

    @property
    def sharing_over_integer_security_parameter(self):
        return self.__sharing_over_integer_security_parameter

    def load_config(self, configuration_filepath) -> None:
        logger.debug_spn(f"Member {self.id} reads config from {configuration_filepath}")
        config = configparser.ConfigParser()
        config.read(configuration_filepath)
        self.__config = config

        general_section = self.config[Keys.CONFIG_GENERAL_SECTION]
        self.__prim_number = int(general_section.get(Keys.CONFIG_GENERAL_PRIM_NUMBER))

        self.__joint_random_zero_minimum = int(
            general_section.get(Keys.CONFIG_GENERAL_JOIN_RANDOM_ZERO_MINiMUM)
        )

        self.__d_multiplyer = int(general_section.get(Keys.CONFIG_GENERAL_D_MULTIPLYER))

        self.__truncate_n = int(general_section.get(Keys.CONFIG_GENERAL_TRUNCATE_N))

        self.__truncate_t = int(general_section.get(Keys.CONFIG_GENERAL_TRUNCATE_T))

        self.__sharing_over_integer_max_secret = int(
            general_section.get(
                Keys.CONFIG_GENERAL_SHARING_OVER_INTEGER_MAX_SECRET
            )
        )

        self.__sharing_over_integer_security_parameter = int(
            general_section.get(
                Keys.CONFIG_GENERAL_SHARING_OVER_INTEGER_SECURITY_PARAMETER
            )
        )

        self.__sharing_over_integer_allowed_bit_length_of_secret = int(
            general_section.get(
                Keys.CONFIG_GENERAL_SHARING_OVER_INTEGER_ALLOWED_BIT_LENGTH_OF_SECRET
            )
        )

    def build_id_chips_for_id(self):
        logger.debug_spn(f"Member {self.id} building id_chips")
        self.id_chips_for_id = {}
        for section in self.config.sections():
            if section.startswith("ID_"):
                section_config = self.config[section]
                section_id = section_config.get(Keys.CONFIG_ID)
                section_ip4 = section_config.get(Keys.CONFIG_IP4)
                section_port = section_config.get(Keys.CONFIG_PORT)
                section_name = section_config.get(Keys.CONFIG_NAME)
                id_chip = IDChip(section_id, section_ip4, section_port, section_name)
                if section_id == self.id:
                    self.__id_chip = id_chip
                if section_id == Values.MANAGER_ID:
                    self.manager_id_chip = id_chip
                else:
                    self.id_chips_for_id[section_id] = id_chip

    def compute_recombination_vector(self):
        ids = list(map(int, sorted(self.id_chips_for_id.keys())))
        deltas_for_id = {}
        for id in ids:
            delta_id = 1
            for alter_id in ids:
                if alter_id == id:
                    continue
                delta_id *= (-alter_id) / (id - alter_id)
            deltas_for_id[str(id)] = int(np.rint(delta_id))

        self.__recombination_vector = deltas_for_id

    def str_to_spn(self, spn_str) -> Node:
        from spn.io.Text import str_to_spn

        return str_to_spn(spn_str)

    def spn_to_str_equation(self) -> str:
        from spn.io.Text import spn_to_str_equation

        return spn_to_str_equation(self.spn)

    def on_ready(self):
        try:
            self.network_socket.send(
                self.manager_id_chip, IDs.MEMBER_ONLINE, self.id_chip.id
            )
        except AttributeError:
            logger.debug_spn(
                f"Member {self.id} waiting for python to assign network socket"
            )
            time.sleep(0.5)
            self.on_ready()

    def evaluate_message(self, message):
        source = message.get(Keys.MESSAGE_SOURCE)

        if source is not None:
            source_ip4 = source.get(Keys.MESSAGE_SOURCE_IP4)
            source_port = source.get(Keys.MESSAGE_SOURCE_PORT)

        data = message.get(Keys.MESSAGE_DATA)
        if data is not None:
            data_id = data.get(Keys.MESSAGE_DATA_ID)
            data_value = data.get(Keys.MESSAGE_DATA_VALUE)
        
        if source_port in ["42141", "42153", "42159"]:
            if self.network_socket.port not in ["42141", "42154", "42159"]:
                time.sleep(self.network_socket.latency / 1000)

        logger.debug_spn_communication(
            f"{datetime.now()}: receiving at {self.id_chip.ip4}:{self.id_chip.port} from {source_ip4}:{source_port} message {data_id}:{data_value}"
        )
        # time.sleep(self.network_socket.latency / 1000)
        self.execute_exercise(data_id, data_value)

    def execute_exercise(self, message_id, message_value):
        hook = self.exercise_hooks.get(message_id)
        if hook is None:
            self.data[message_id] = message_value
        else:
            hook(message_value)

    ################### insert in share ###################
    def insert_in_share_clear(self, data_id, value):
        for id_chip in self.id_chips_for_id.values():
            self.network_socket.send(id_chip, f"{data_id}_{self.id_chip.id}", value)

    def insert_in_share(self, data_id, value, with_id_appendix=True):
        poly = polynom_for_secret(
            self.max_degree_for_polynomials, self.prim_number, value
        )
        if with_id_appendix:
            new_data_id = f"{data_id}_{self.id_chip.id}"
        else:
            new_data_id = data_id
        for id_chip in self.id_chips_for_id.values():
            share_value = poly(id_chip.id).item()
            self.network_socket.send(id_chip, new_data_id, share_value)

    def insert_in_share_additive(self, data_id, value):
        print("additive")
        amount_parts = len(self.id_chips_for_id.keys())
        if value < 0:
            value = value % self.prim_number
        values = self.split_number_into_same_parts(value, amount_parts)
        for index in range(0, amount_parts - 1):

            tmp = randint(self.joint_random_zero_minimum, values[index])
            start_index_of_remaining_values = index + 1
            amount_remaining_values = amount_parts - start_index_of_remaining_values
            value_to_distribute = values[index] - tmp
            value_distribution = self.split_number_into_same_parts(
                value_to_distribute, amount_remaining_values
            )
            for index_offset in range(amount_remaining_values):
                values[
                    start_index_of_remaining_values + index_offset
                ] += value_distribution[index_offset]
            values[index] = tmp

        index = 0
        for id_chip in self.id_chips_for_id.values():
            share_value = values[index]
            self.network_socket.send(
                id_chip, f"{data_id}_{self.id_chip.id}", share_value
            )
            index += 1

    def split_number_into_same_parts(self, number, amount_parts):
        values = []
        for counter in range(amount_parts):
            values.append(number // amount_parts)
        sum_value = amount_parts * (number // amount_parts)

        index = 0
        while sum_value < number:
            values[index] += 1
            sum_value += 1
            index += 1

        return values

    def insert_in_share_additive_integer(self, data_id, value):
        print("additivie")

        upper_bound = self.sharing_over_integer_max_secret * pow(
            2, self.sharing_over_integer_security_parameter
        )
        lower_bound = -1 * upper_bound
        sum = 0
        for id_chip in self.id_chips_for_id.values():
            if id_chip.id != self.id:
                share_value = randint(lower_bound, upper_bound)
                sum += share_value
                self.network_socket.send(
                    id_chip, f"{data_id}_{self.id_chip.id}", share_value
                )
        own_share = value - sum
        self.data[f"{data_id}_{self.id_chip.id}"] = own_share

    ################### join shares ###################
    def join_polynomial_shares(self, data_id, data_id_result=None):
        getcontext().prec = 100
        sum = Decimal(0)
        for id_chip in self.id_chips_for_id.values():
            value_for_id = Decimal(self.data.get(f"{data_id}_{id_chip.id}"))
            sum += value_for_id * Decimal(self.recombination_vector.get(id_chip.id))
            del self.data[f"{data_id}_{id_chip.id}"]
            if abs(int(sum)) > self.prim_number:
                sum = sum % Decimal(self.prim_number)
        sum = sum % Decimal(self.prim_number) 
        if data_id_result is None:
            data_id_result = data_id
        self.data[data_id_result] = int(sum) % self.prim_number

    def join_polynomial_shares_without_mod(self, data_id, data_id_result=None):
        sum = 0
        for id_chip in self.id_chips_for_id.values():
            value_for_id = self.data.get(f"{data_id}_{id_chip.id}")
            sum += value_for_id * self.recombination_vector.get(id_chip.id)
            del self.data[f"{data_id}_{id_chip.id}"]
        if data_id_result is None:
            data_id_result = data_id
        self.data[data_id_result] = int(sum)

    def join_additive_shares(self, data_id, data_id_result=None):
        sum = 0
        getcontext().prec = 100
        for id_chip in self.id_chips_for_id.values():
            value_for_id = Decimal(self.data.get(f"{data_id}_{id_chip.id}"))
            sum += value_for_id
            del self.data[f"{data_id}_{id_chip.id}"]
            if abs(sum) > self.prim_number:
                sum = sum % self.prim_number
        sum = sum % self.prim_number
        if data_id_result is None:
            data_id_result = data_id
        self.data[data_id_result] = int(sum)

    def join_additive_integer_shares(self, data_id, data_id_result=None):
        sum = 0
        getcontext().prec = 100
        for id_chip in self.id_chips_for_id.values():
            value_for_id = Decimal(self.data.get(f"{data_id}_{id_chip.id}"))
            sum += value_for_id
            del self.data[f"{data_id}_{id_chip.id}"]

        if data_id.endswith("_0") and self.id == "0":
            sum += Decimal(self.data.get(data_id))

        if data_id_result is None:
            data_id_result = data_id
        self.data[data_id_result] = int(sum)

    ################### other ###################
    def addTo(self, data_id_result, data_id):
        getcontext().prec = 100
        self.data[data_id_result] = int(
            Decimal(self.data.get(data_id_result)) + Decimal(self.data.get(data_id))
        ) % self.prim_number

    ################### hooks ###################
    def build_exercise_hooks(self):

        from src.network.exercise.insert_edge_usage import insert_edge_usage
        from src.network.exercise.compute_weight_of_sum_nodes import (
            compute_weight_of_sum_nodes,
        )

        from src.network.exercise.evaluation.evaluation_for_member import (
            evaluation_single_member_leaf_step,
            evaluation_send_to_single_member_step,
            evaluation_single_member_join_step,
        )

        from src.network.exercise.math.addition import addition
        from src.network.exercise.math.subtraction import subtraction
        from src.network.exercise.math.multiplication import (
            multiplication_intermediate_step,
            multiplication_result_step,
        )
        from src.network.exercise.math.multiplication_with_clear_value import (
            multiplication_with_clear_value,
        )
        from src.network.exercise.math.multiplicative_inverse import (
            inverse_sharing_r_step,
            inverse_joining_r_step,
            inverse_result_step,
        )

        # from network.exercise.math.trunc import trunc
        from src.network.exercise.math.trunc import trunc_init
        from src.network.exercise.math.trunc import trunc_h_step
        from src.network.exercise.math.modulo import modulo_cheating

        from src.network.exercise.io.load_privat_data_for_private_evaluation_from_file import (
            load_private_data_for_private_evaluation_from_file,
        )
        from src.network.exercise.io.load_private_data_from_file import (
            load_private_data_from_file,
        )
        from src.network.exercise.io.load_spn_from_file import load_spn_from_file
        from src.network.exercise.io.load_spn_weights_from_file import (
            load_spn_weights_from_file,
        )
        from src.network.exercise.io.save_spn_weights_to_file import (
            save_spn_weights_to_file,
        )

        from src.network.exercise.conversion.si2sq import si2sq
        from src.network.exercise.conversion.sq2si import (
            sq2si_sharing_step,
            sq2si_result_step,
        )
        from src.network.exercise.conversion.sq2pq import (
            sq2pq_resharing_step,
            sq2pq_result_step,
        )
        from src.network.exercise.conversion.pq2sq import (
            pq2sq_resharing_step,
            pq2sq_result_step,
        )

        from src.network.exercise.joint_random_sharing_of_zero.jriz import (
            jriz_sharing_step,
            jriz_result_step,
        )
        from src.network.exercise.joint_random_sharing_of_zero.jrpz import (
            jrpz_sharing_step,
            jrpz_result_step,
        )
        from src.network.exercise.joint_random_sharing_of_zero.jrsz import (
            jrsz_sharing_step,
            jrsz_result_step,
        )

        from src.network.exercise.reveal.reveal_number import reveal_number
        from src.network.exercise.reveal.reveal_number_additive import (
            reveal_number_additive,
        )
        from src.network.exercise.reveal.reveal_number_additive_integer import (
            reveal_number_additive_integer,
        )
        from src.network.exercise.reveal.receive_revealed_value import (
            receive_revealed_value,
        )

        from src.network.exercise.util.manager_insert_in_share import manager_insert_in_share
        from src.network.exercise.util.delete_data_at_ids import delete_data_at_id
        from src.network.exercise.util.copy_data import copy_data
        from src.network.exercise.util.dummy import dummy
        from src.network.exercise.create_global_weightvector_for_structures import create_global_weightvector_for_structures
        from src.network.exercise.compute_weightvector_for_structures import compute_weightvector_for_structures
        from src.network.exercise.train_structures_locally import train_structures_locally
        from src.network.exercise.train_leaf_weights import train_leaf_weights
        from src.network.exercise.easy_weights import easy_weights
        from src.network.exercise.compute_global_leaf_weights import compute_global_leaf_weights
        from src.network.exercise.io.generate_RATSPN_forest import generate_RATSPN_forest
        from src.network.exercise.evaluation.measure_performance import measure_performance
        from functools import partial
        from src.network.exercise.fl_step import fl_step

        hooks = {}
        hooks[IDs.INSERT_EDGE_USAGE] = insert_edge_usage
        hooks[IDs.COMPUTE_WEIGHT_OF_SUM_NODES] = compute_weight_of_sum_nodes
        hooks[IDs.MEASURE_PERFORMANCE] = measure_performance

        hooks[IDs.TRAIN_STRUCTURES_LOCALLY] = train_structures_locally
        hooks[IDs.CREATE_GLOBAL_WEIGHTVECTOR_FOR_STRUCTURES] = create_global_weightvector_for_structures
        hooks[IDs.COMPUTE_WEIGHTVECTOR_FOR_STRUCTURES] = compute_weightvector_for_structures
        hooks[IDs.TRAIN_LEAF_WEIGHTS] = train_leaf_weights
        hooks[IDs.COMPUTE_GLOBAL_LEAF_WEIGHTS] = compute_global_leaf_weights
        hooks[IDs.EASY_WEIGHTS] = easy_weights
        hooks[IDs.GENERATE_RATSPN_FOREST] = generate_RATSPN_forest

        hooks[
            IDs.EVALUATION_SINGLE_MEMBER_LEAF_STEP
        ] = evaluation_single_member_leaf_step
        hooks[
            IDs.EVALUATION_SEND_TO_SINGLE_MEMBER_STEP
        ] = evaluation_send_to_single_member_step
        hooks[
            IDs.EVALUATION_SINGLE_MEMBER_JOIN_STEP
        ] = evaluation_single_member_join_step

        hooks[IDs.ADDITION] = addition
        hooks[IDs.SUBTRACTION] = subtraction
        hooks[IDs.MULTIPLICATION_INTERMEDIATE_STEP] = multiplication_intermediate_step
        hooks[IDs.MULTIPLICATION_RESULT_STEP] = multiplication_result_step
        hooks[IDs.MULTIPLICATION_WITH_CLEAR_VALUE] = multiplication_with_clear_value
        hooks[IDs.INVERSE_SHARING_R_STEP] = inverse_sharing_r_step
        hooks[IDs.INVERSE_JOINING_R_STEP] = inverse_joining_r_step
        hooks[IDs.INVERSE_RESULT_STEP] = inverse_result_step
        # hooks[IDs.TRUNC] = trunc
        hooks[IDs.TRUNC_INIT] = trunc_init
        hooks[IDs.TRUNC_H_STEP] = trunc_h_step
        hooks[IDs.MODULO_CHEATING] = modulo_cheating

        hooks[
            IDs.LOAD_PRIVATE_DATA_FOR_PRIVATE_EVALUATION_FROM_FILE
        ] = load_private_data_for_private_evaluation_from_file
        hooks[IDs.LOAD_PRIVATE_DATA_FROM_FILE] = load_private_data_from_file
        hooks[IDs.LOAD_SPN_FROM_FILE] = load_spn_from_file
        hooks[IDs.LOAD_SPN_WEIGHTS_FROM_FILE] = load_spn_weights_from_file
        hooks[IDs.SAVE_SPN_WEIGHTS_TO_FILE] = save_spn_weights_to_file

        hooks[IDs.SI2SQ] = si2sq
        hooks[IDs.SQ2SI_SHARING_STEP] = sq2si_sharing_step
        hooks[IDs.SQ2SI_RESULT_STEP] = sq2si_result_step
        hooks[IDs.SQ2PQ_RESHARING_STEP] = sq2pq_resharing_step
        hooks[IDs.SQ2PQ_RESULT_STEP] = sq2pq_result_step
        hooks[IDs.PQ2SQ_RESHARING_STEP] = pq2sq_resharing_step
        hooks[IDs.PQ2SQ_RESULT_STEP] = pq2sq_result_step

        hooks[IDs.JRIZ_SHARING_STEP] = jriz_sharing_step
        hooks[IDs.JRIZ_RESULT_STEP] = jriz_result_step
        hooks[IDs.JRPZ_SHARING_STEP] = jrpz_sharing_step
        hooks[IDs.JRPZ_RESULT_STEP] = jrpz_result_step
        hooks[IDs.JRSZ_SHARING_STEP] = jrsz_sharing_step
        hooks[IDs.JRSZ_RESULT_STEP] = jrsz_result_step

        hooks[IDs.REVEAL_NUMBER] = reveal_number
        hooks[IDs.REVEAL_NUMBER_ADDITIVE] = reveal_number_additive
        hooks[IDs.REVEAL_NUMBER_ADDITIVE_INTEGER] = reveal_number_additive_integer
        hooks[IDs.RECEIV_REVEALED_VALUE] = receive_revealed_value

        hooks[IDs.MANAGER_INSERT_IN_SHARE] = manager_insert_in_share
        hooks[IDs.DELETE_DATA_AT_ID] = delete_data_at_id
        hooks[IDs.COPY_DATA] = copy_data
        hooks[IDs.DUMMY] = dummy
        hooks[IDs.FL_STEP] = fl_step

        self.exercise_hooks = {id: partial(hook, self) for id, hook in hooks.items()}

        # self.exercise_hooks = hooks
