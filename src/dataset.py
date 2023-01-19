import numpy as np
import os
import csv
import subprocess
from spn.algorithms.Inference import log_likelihood
from spn.structure.Base import Context
from spn.structure.leaves.parametric.Parametric import Categorical, Gaussian
from spn.algorithms.LearningWrappers import learn_classifier, learn_parametric

DEBD = [
    "accidents",
    "ad",
    "baudio",
    "bbc",
    "bnetflix",
    "book",
    "c20ng",
    "cr52",
    "cwebkb",
    "dna",
    "jester",
    "kdd",
    "kosarek",
    "msnbc",
    "msweb",
    "nltcs",
    "plants",
    "pumsb_star",
    "tmovie",
    "tretail",
]


DEBD_num_vars = {
    "accidents": 111,
    "ad": 1556,
    "baudio": 100,
    "bbc": 1058,
    "bnetflix": 100,
    "book": 500,
    "c20ng": 910,
    "cr52": 889,
    "cwebkb": 839,
    "dna": 180,
    "jester": 100,
    "kdd": 64,
    "kosarek": 190,
    "msnbc": 17,
    "msweb": 294,
    "nltcs": 16,
    "plants": 69,
    "pumsb_star": 163,
    "tmovie": 500,
    "tretail": 135,
}


DEBD_display_name = {
    "accidents": "accidents",
    "ad": "ad",
    "baudio": "audio",
    "bbc": "bbc",
    "bnetflix": "netflix",
    "book": "book",
    "c20ng": "20ng",
    "cr52": "reuters-52",
    "cwebkb": "web-kb",
    "dna": "dna",
    "jester": "jester",
    "kdd": "kdd-2k",
    "kosarek": "kosarek",
    "msnbc": "msnbc",
    "msweb": "msweb",
    "nltcs": "nltcs",
    "plants": "plants",
    "pumsb_star": "pumsb-star",
    "tmovie": "each-movie",
    "tretail": "retail",
}

# https://github.com/arranger1044/DEBD
def maybe_download_DEBD(data_dir):
    if os.path.isdir(data_dir):
        print("DEBD already exists")
        return
    subprocess.run(["git", "clone", "https://github.com/arranger1044/DEBD", data_dir])
    wd = os.getcwd()
    os.chdir(data_dir)
    subprocess.run(["git", "checkout", "80a4906dcf3b3463370f904efa42c21e8295e85c"])
    subprocess.run(["rm", "-rf", ".git"])
    os.chdir(wd)


def load_debd_dataset(data_dir, name, dtype="int32"):
    """Load one of the twenty binary density esimtation benchmark datasets."""

    train_path = os.path.join(data_dir, "datasets", name, name + ".train.data")
    test_path = os.path.join(data_dir, "datasets", name, name + ".test.data")
    valid_path = os.path.join(data_dir, "datasets", name, name + ".valid.data")

    reader = csv.reader(open(train_path, "r"), delimiter=",")
    train_x = np.array(list(reader)).astype(dtype)

    reader = csv.reader(open(test_path, "r"), delimiter=",")
    test_x = np.array(list(reader)).astype(dtype)

    reader = csv.reader(open(valid_path, "r"), delimiter=",")
    valid_x = np.array(list(reader)).astype(dtype)

    return train_x, test_x, valid_x


def learn_debd_spn(data_dir, debd_dataset_name):
    # data_dir = "/mnt/d/datasets/DEDB"
    maybe_download_DEBD(data_dir)
    train_x, test_x, valid_x = load_debd_dataset(data_dir, debd_dataset_name)
    ds_context = Context(parametric_types=[Categorical] * train_x.shape[1])
    ds_context.add_domains(train_x)

    spn = learn_parametric(train_x, ds_context)

    return train_x, test_x, valid_x, spn


from spn.structure.Base import get_nodes_by_type
from spn.io.Text import spn_to_str_equation, str_to_spn
from spn.structure.Base import Sum, Product, Leaf
import math
from mathy.polynomial import polynom_for_secret

from pathlib import Path


def save_debd_spn(data_dir, debd_dataset_name, save_location):
    Path(save_location).mkdir(parents=True, exist_ok=True)
    # private_data_folderpath = f"{save_location}/private_data"
    # spn_folderpath = f"{save_location}/spn"
    # spn_weights_folderpath = f"{save_location}/spn_weights"
    # private_data_for_evaluation_folderpath = f"{save_location}/private_data_for_evaluation"

    train_x, test_x, valid_x, spn = learn_debd_spn(data_dir, debd_dataset_name)
    eval_x = np.concatenate((test_x, valid_x), axis=0)
    print(train_x.shape)
    print(eval_x.shape)

    # from spn.gpu.TensorFlow import eval_tf
    # lltf = eval_tf(spn, eval_x)

    np_expo = lambda x: np.exp(x)
    vfunc = np.vectorize(np_expo)

    loglike = log_likelihood(spn, eval_x)
    print(loglike, np.exp(loglike))
    target = vfunc(loglike)

    # out = np.array(map(np.exp, loglike))

    np.savetxt(f"{save_location}/target_values.out", target)  # fmt="%i"

    ##trainings_data_splitted = np.array_split(train_x, len(ids))
    ##for id_index in range(len(ids)):
    ##    id = ids[id_index]
    # file = open(f"{save_location}/private_data_{id}.in", "w+")
    # file.write(trainings_data_splitted[id_index])
    # file.flush()
    # file.close()
    ##    np.savetxt(
    ##        f"{save_location}/private_data_{id}.in",
    ##        trainings_data_splitted[id_index],
    ##        fmt="%i",
    ##    )

    ##evaluation_data_splitted = np.array_split(eval_x, len(ids))
    ##for id_index in range(len(ids)):
    ##    id = ids[id_index]
    # file = open(f"{save_location}/private_data_for_evaluation_{id}.in", "w+")
    # file.write(evaluation_data_splitted[id_index])
    # file.flush()
    # file.close()
    ##    np.savetxt(
    ##        f"{save_location}/private_data_for_evaluation_{id}.in",
    ##        evaluation_data_splitted[id_index],
    ##        fmt="%i",
    ##    )

    ##spn_str = spn_to_str_equation(spn)
    ##spn_2 = str_to_spn(spn_str)
    ##spn_str_2 = spn_to_str_equation(spn_2)

    ##file = open(f"{save_location}/spn.in", "w+")
    ##file.write(spn_str_2)
    ##file.flush()
    ##file.close()

    ##d_multiplyer = 1000000000
    ##max_degree_for_polynomials = len(ids) // 2
    ##prim_number = 13558774610046711780701

    ##for sum_node in get_nodes_by_type(spn_2, Sum):
    ##    for index in range(len(sum_node.children)):
    ##        child_node = sum_node.children[index]
    ##        data_id = f"({sum_node.id}, {child_node.id})"
    ##        exact_weight = sum_node.weights[index]
    ##        digits = int(math.log(d_multiplyer, 10) / 2)
    ##        exact_weight_rounded = round(exact_weight, digits - 1)
    ##        weight_to_insert = int(exact_weight_rounded * d_multiplyer)
    ##        print(
    ##            f"For {data_id} we insert {exact_weight_rounded}*d from {exact_weight}"
    ##        )

    ##        poly = polynom_for_secret(
    ##            max_degree_for_polynomials, prim_number, weight_to_insert
    ##        )

    ##        for id_index in range(len(ids)):
    ##            id = ids[id_index]
    ##            share_value = poly(id).item()
    ##            file = open(f"{save_location}/spn_weights_{id}.in", "a+")
    ##            if id_index == len(ids) - 1:
    ##                content = f"{data_id}={share_value}"
    ##            else:
    ##                content = f"{data_id}={share_value}\n"
    ##            file.write(content)
    ##            file.flush()
    ##            file.close()


data_dir = "./data"
save_location_base = "./resources/input"
##ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

from tqdm import tqdm

DEBD_REDUCED = [
    "accidents",  #  3.60 MB
    "baudio",  #  9.73 MB   out of time
    "bbc",  #  4.48 MB  over 2h
    "bnetflix",  #  3.81 MB
    "book",  # 11.00 MB
    "c20ng",  # 32.60 MB
    "cr52",  # 15.40 MB
    "cwebkb",  #  6.71 MB
    "dna",  #  1.09 MB  fast
    "jester",  #  2.69 MB fast
    "kdd",  # 28.66 MB
    "kosarek",  # 16.10 MB
    "msnbc",  # 12.50 MB
    "msweb",  # 21.10 MB
    "nltcs",  #  0.67 MB
    "plants",  #  3.05 MB medium
    "pumsb_star",  #  5.08 MB
    "tmovie",  #  5.83 MB
    "tretail",  #  7.56 MB
]

# dedb_with_progress_bar = tqdm(DEBD)
# "baudio",
#    "bbc",
#    "bnetflix",
#    "book",
#    "c20ng",

# for debd_dataset_name in dedb_with_progress_bar:
#    dedb_with_progress_bar.set_description(f"Processing {debd_dataset_name}")
debd_dataset_name = "dna"
save_location = f"{save_location_base}/{debd_dataset_name}"
save_debd_spn(data_dir, debd_dataset_name, save_location)


# train_x, test_x, valid_x, spn = learn_debd_spn(data_dir, debd_dataset_name)
# print(type(train_x))
# print(train_x.shape)
# (16181, 16)
