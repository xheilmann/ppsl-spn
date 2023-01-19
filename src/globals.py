class Keys:

    ##### General section #####
    CONFIG_GENERAL_PRIVATE = "private"
    CONFIG_GENERAL_GENERATE_SPN_STRUCTURES = "generate_spn_structures"
    CONFIG_GENERAL_SECTION = "General"
    CONFIG_GENERAL_PRIM_NUMBER = "prim_number"

    CONFIG_GENERAL_JOIN_RANDOM_ZERO_MINiMUM = (
        "joint_random_zero_minimum"
    )
    CONFIG_GENERAL_D_MULTIPLYER = "d_multiplyer"
    CONFIG_GENERAL_TRUNCATE_N = "truncate_n"
    CONFIG_GENERAL_TRUNCATE_T = "truncate_t"
    CONFIG_GENERAL_SHARING_OVER_INTEGER_MAX_SECRET = (
        "sharing_over_integer_max_secret"
    )
    CONFIG_GENERAL_SHARING_OVER_INTEGER_SECURITY_PARAMETER = (
        "sharing_over_integer_security_parameter"
    )
    CONFIG_GENERAL_SHARING_OVER_INTEGER_ALLOWED_BIT_LENGTH_OF_SECRET = (
        "sharing_over_integer_allowed_bit_length_of_secret"
    )

    CONFIG_GENERAL_LOAD_SPN_WEIGHTS = "load_spn_weights"
    CONFIG_GENERAL_SAVE_SPN_WEIGHTS = "save_spn_weights"

    CONFIG_GENERAL_NUM_LOCAL_ITERATIONS = "num_local_iterations"

    CONFIG_GENERAL_RAT_SPN_DICTIONARY = "ratspn_dictionary"
    CONFIG_GENERAL_NUM_DIMS = "num_dims"
    CONFIG_GENERAL_OUTPUT_FILE_PATH = "output_file_path"


    ##### ID Section #####
    CONFIG_ID = "id"
    CONFIG_IP4 = "ip4"
    CONFIG_PORT = "port"
    CONFIG_NAME = "name"
    CONFIG_LATENCY = "latency"
    CONFIG_PRIVATE_EVALUATION = "private_evaluation"
    CONFIG_PRIVATE_EVALUATION_AMOUNT_LINES_TO_EVALUATE = (
        "private_evaluation_amount_lines_to_evaluate"
    )
    CONFIG_PRIVATE_DATA_FILE_PATH = "private_data_file_path"
    CONFIG_SPN_FILE_PATH = "spn_file_path"
    CONFIG_SPN_WEIGHTS_FILE_PATH = "spn_weights_file_path"
    CONFIG_PRIVATE_DATA_FOR_EVALUATION_FILE_PATH = (
        "private_data_for_evaluation_file_path"
    )

    MESSAGE_SOURCE = "source"
    MESSAGE_SOURCE_IP4 = "ip4"
    MESSAGE_SOURCE_PORT = "port"

    MESSAGE_DATA = "data"
    MESSAGE_DATA_ID = "id"
    MESSAGE_DATA_VALUE = "value"
    CONFIG_CKPTS_FILE_PATH = "saving_checkpoints_file_path"
    CONFIG_GLOBAL_DATA_FOR_EVALUATION_FILE_PATH = "global_data_for_evaluation_file_path"

    # MESSAGE_ONLINE_ID = "id"


class DataIDs:
    JRSZ_FOR_NUMERATOR = "JRSZ_for_numerator"
    JRSZ_FOR_DENOMINATOR = "JRSZ_for_denominator"

    DIVISION_MULTIPLYER = "division_multiplyer"
    DIVISION_MULTIPLYER_APPINVERSE = "division_multiplyer_appinverse"

    APPINVERSE_OF_TWO_POW_T_PLUS_1 = "appinverse_of_two_pow_t_plus_1"
    APPINVERSE_OF_TWO_POW_N_MINUS_1 = "appinverse_of_two_pow_n_minus_1"
    
    TEST_X = 'test_x'
    TEST_Y = 'test_y'
    DEVI = 'devi'
    DEVI_TEST = 'devi_test'
    DEVI2 = 'devi2'
    DEVI_TEST2 = 'devi_test2'


class IDs:
    FL_STEP = "fl_step"
    GENERATE_RATSPN_FOREST = "generate_RATSPN_forest"
    EASY_WEIGHTS = "easy_weights"
    COMPUTE_GLOBAL_LEAF_WEIGHTS = "compute_global_leaf_weights"
    TRAIN_LEAF_WEIGHTS = "train_leaf_weights"
    TRAIN_STRUCTURES_LOCALLY = "train_structures_locally"
    MEASURE_PERFORMANCE = "measure_performance"
    MEMBER_ONLINE = "member_online"

    LOAD_SPN_FROM_FILE = "load_spn_from_file"
    LOAD_PRIVATE_DATA_FROM_FILE = "load_private_data_from_file"
    LOAD_PRIVATE_DATA_FOR_PRIVATE_EVALUATION_FROM_FILE = (
        "load_private_data_for_private_evaluation_from_file"
    )
    SAVE_SPN_WEIGHTS_TO_FILE = "save_spn_weights_to_file"
    LOAD_SPN_WEIGHTS_FROM_FILE = "load_spn_weights_from_file"

    MANAGER_INSERT_IN_SHARE = "manager_insert_in_share"

    INSERT_EDGE_USAGE = "insert_edge_usage"
    COMPUTE_WEIGHT_OF_SUM_NODES = "compute_weight_of_sum_nodes"

    REVEAL_NUMBER = "reveal_number"
    REVEAL_NUMBER_ADDITIVE = "reveal_number_additive"
    REVEAL_NUMBER_ADDITIVE_INTEGER = "reveal_number_additive_integer"

    RECEIV_REVEALED_VALUE = "receive_revealed_value"

    ADDITION = "addition"
    SUBTRACTION = "subtraction"
    MODULO_CHEATING = "modulo_cheating"

    MULTIPLICATION_INTERMEDIATE_STEP = "multiplication_intermediate_step"
    MULTIPLICATION_RESULT_STEP = "multiplication_result_step"

    MULTIPLICATION_WITH_CLEAR_VALUE = "multiplication_with_clear_value"

    SQ2PQ_RESHARING_STEP = "sq2pq_resharing_step"
    SQ2PQ_RESULT_STEP = "sq2pq_result_step"

    PQ2SQ_RESHARING_STEP = "pq2sq_resharing_step"
    PQ2SQ_RESULT_STEP = "pq2sq_result_step"

    SI2SQ = "si2sq"
    SQ2SI_SHARING_STEP = "sq2si_sharing_step"
    SQ2SI_RESULT_STEP = "sq2si_result_step"

    JRIZ_SHARING_STEP = "jriz_sharing_step"
    JRIZ_RESULT_STEP = "jriz_result_step"

    JRPZ_SHARING_STEP = "jrpz_sharing_step"
    JRPZ_RESULT_STEP = "jrpz_result_step"

    JRSZ_SHARING_STEP = "jrsz_sharing_step"
    JRSZ_RESULT_STEP = "jrsz_result_step"

    JRP_SHARING_STEP = "jrp_sharing_step"
    JRP_RESULT_STEP = "jrp_result_step"

    TRUNC = "trunc"
    TRUNC_INIT = "trunc_init"
    TRUNC_H_STEP = "trunc_h_step"

    TRUNC_X_ADD_R_STEP = "trunc_x_add_r_step"
    TRUNC_RESULT_STEP = "trunc_result_step"

    APPROX_INVERSE = "approx_inverse"

    INVERSE_SHARING_R_STEP = "inverse_sharing_r_step"
    INVERSE_JOINING_R_STEP = "inverse_joining_r_step"
    # INVERSE_MULTIPLICATION_STEP = "inverse_multiplication_step"
    INVERSE_RESULT_STEP = "inverse_result_step"

    EVALUATION_SINGLE_MEMBER_LEAF_STEP = "evaluation_single_member_leaf_step"
    EVALUATION_SEND_TO_SINGLE_MEMBER_STEP = "evaluation_send_to_single_member_step"
    EVALUATION_SINGLE_MEMBER_JOIN_STEP = "evaluation_single_member_join_step"

    DELETE_DATA_AT_ID = "delete_data_at_id"
    COPY_DATA = "copy_data"
    DUMMY = "dummy"

    CREATE_GLOBAL_WEIGHTVECTOR_FOR_STRUCTURES = "create_global_weightvector_for_structures"
    COMPUTE_WEIGHTVECTOR_FOR_STRUCTURES = "compute_weightvector_for_structures"


class Values:
    MANAGER_ID = "0"
