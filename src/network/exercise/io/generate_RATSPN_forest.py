from spn.io.Text import spn_to_str_equation

from src.RatSPN.RatSpn import RatSpn
from src.RatSPN.RegionGraph import RegionGraph

from spn.algorithms.TransformStructure import Compress, SPN_Reshape, Copy
from spn.structure.leaves.parametric.Parametric import Categorical, MultivariateGaussian, Gaussian, Bernoulli
import numpy as np
from spn.structure.Base import Sum, Product, get_nodes_by_type, Leaf
from spn.structure.Base import assign_ids, rebuild_scopes_bottom_up
from src.network.exercise.exercise_class import Exercise
from src.globals import IDs, Keys
from src.network.exercise.util.copy_data import add_exercise_copy_data
from src.network.exercise.io.load_spn_from_file import add_exercise_load_spn_from_file
import tensorflow
import pickle


def add_exercise_generate_RATSPN_forest(manager):
    """
    generates the initial RAT-SPN forest based on the RAT-SPN dictionary input
    """
    initialize_RATSPN_forest(manager)
    manager.exercises.append(Exercise(IDs.GENERATE_RATSPN_FOREST))
    add_exercise_load_spn_from_file(manager)

def generate_RATSPN_forest(member, message):
    config_dict_file = member.config[Keys.CONFIG_GENERAL_SECTION].get(
        Keys.CONFIG_GENERAL_RAT_SPN_DICTIONARY)
    myfile = open(config_dict_file, 'r')
    member.structure_config = []
    for line in myfile:
        line_dict = {}
        list = [a for a in line.strip().split(',')]
        for entry in list:
            k, v = entry.split(":")
            line_dict[k.strip()] = int(v.strip())

        member.structure_config.append(line_dict)

    myfile.close()
    
    #print(member.structure_config)

    member.network_socket.send(
        member.manager_id_chip,
        IDs.GENERATE_RATSPN_FOREST,
        member.id,
    )

def initialize_RATSPN_forest(member):
    member.spn = []
    config_dict_file = member.config[Keys.CONFIG_GENERAL_SECTION].get(
        Keys.CONFIG_GENERAL_RAT_SPN_DICTIONARY)
    myfile = open(config_dict_file, 'r')
    structure_config = []
    member.leaf_stats = {}
    for line in myfile:
        line_dict = {}
        list = [a for a in line.strip().split(',')]
        for entry in list:
            k, v = entry.split(":")
            line_dict[k.strip()] = int(v.strip())

        structure_config.append(line_dict)

    myfile.close()
    i = 0
    
    # Make Region Graph
    for structure_config in structure_config:

        num_dims = int(member.config[Keys.CONFIG_GENERAL_SECTION].get(
        Keys.CONFIG_GENERAL_NUM_DIMS
        ))
        num_recursive_splits = structure_config.get("num_recursive_splits")
        num_classes = num_dims
        num_sums = structure_config.get('num_sums')
        num_input_distributions = structure_config.get('num_input_distributions')
        split_depth = structure_config.get('split_depth')


        region_graph = RegionGraph(range(0, num_dims), np.random.randint(0, 1000000000))
        for _ in range(0, num_recursive_splits):
            region_graph.random_split(2, split_depth)
        region_graph_layers = region_graph.make_layers()

        # Make Tensorflow model
        rat_spn = RatSpn(region_graph_layers, num_classes, num_input_distributions=num_input_distributions, num_sums=num_sums)
        print(rat_spn)
        new_spn = convert_reduced_ratspn_to_spfflow(rat_spn, Bernoulli)
        member.spn.append(new_spn)
        filename = member.config[f"ID_{member.id}"].get(Keys.CONFIG_SPN_FILE_PATH)
        if member.config[Keys.CONFIG_GENERAL_SECTION].get(
            Keys.CONFIG_GENERAL_GENERATE_SPN_STRUCTURES
        ) in ["True", "true"]:
            #stripped_spn = strip_nodes(new_spn, rat_spn)
            with open(f"{filename}/structure_{i}", "wb") as f:
                pickle.dump(new_spn, f) 
        leaf_stats = []
        for l in rat_spn.layers:
            if rat_spn.types[l[0]] == "product":
                leaf_stats.append((sum([int(t.shape[1]) for t in l]))/len(l))

        member.leaf_stats[i] = leaf_stats
        i += 1
        tensorflow.keras.backend.clear_session()
    print(member.leaf_stats)


def write_ratspn_as_equationFile(spn, filename):
    spn_string = spn_to_str_equation(spn)
    f = open(filename, "w")
    f.write(spn_string)
    f.close()

def extract_number(layer_name):
    temp = layer_name.split("/")
    temp1 = temp[1].split("X")
    if temp1[0].startswith("discrete"):
        final1 = temp1[0].lstrip("discrete")
        final2 = temp1[1].lstrip("discrete")
        return int(final1), int(final2)
    if temp1[0].startswith("sum"):
        final1 = temp1[0].lstrip("sum").split("_")
        final2 = temp1[1].lstrip("sum").split("_")
        return int(final1[-1]), int(final2[-1])

def strip_nodes(spn, rat_spn):
    new_children = []
    leaf_stats = []
    for l in rat_spn.layers:
        if rat_spn.types[l[0]] == "product":
            leaf_stats.append((sum([int(t.shape[1]) for t in l])) / len(l))
    for i in range(len(spn.children)):
        if i % leaf_stats[-1] == 0:
            new_children.append(Copy(spn.children[i]))
    new_spn = Sum(weights=[1/len(new_children) for k in range(len(new_children))], children=new_children)
    assign_ids(new_spn)
    rebuild_scopes_bottom_up(new_spn)
    return new_spn


def convert_reduced_ratspn_to_spfflow(spn, leaftype):
    spfflow_layers = []
    for i in range(len(spn.layers) - 1):
        if i == 0:
            layer = []
            for nodes in spn.region_graph_layers[i]:
                sublayer = []
                for j in range(spn.num_input_distributions):
                    subsublayer = []
                    for scope in range(len(nodes)):
                        if leaftype == Bernoulli:
                            subsublayer.append(Bernoulli(p = 0.1, scope=int(nodes[scope])))
                        else:
                            subsublayer.append(Gaussian(mean=0.5, stdev=0.1, scope=int(nodes[scope])))
                    sublayer.append(subsublayer)
                layer.append(sublayer)
            spfflow_layers.append(layer)
        if i == 1:
            layer = []
            for j in range(len(spn.layers[i])):
                sublayer = []
                child1_layer, child2_layer = extract_number(spn.layers[i][j].name)
                for k in range(len(spfflow_layers[i - 1][child1_layer])):
                    child1 = spfflow_layers[i - 1][child1_layer][k]
                    child2 = spfflow_layers[i - 1][child2_layer][k]
                    copy = [Copy(j) for j in child1+child2]
                    pnode = Product(children=copy)
                    rebuild_scopes_bottom_up(pnode)
                    sublayer.append(pnode)
                    if k==2:
                        break
                layer.append(sublayer)
            spfflow_layers.append(layer)

        if i % 2 != 0 and i != 1:
            layer = []
            for j in range(len(spn.layers[i])):
                sublayer = []
                child1_layer, child2_layer = extract_number(spn.layers[i][j].name)
                for child1 in spfflow_layers[i - 1]:
                    #print(spn.region_graph_layers[i-1][child1_layer])
                    if set(child1[0].scope) == set(list(spn.region_graph_layers[i-1][child1_layer])):
                        #child1_unsorted_layer = child1
                        for child2 in spfflow_layers[i - 1]:
                            if set(child2[0].scope) == set(list(spn.region_graph_layers[i-1][child2_layer])):
                                #child2_unsorted_layer = child2
                                for k in range(len(child1)):
                                    small_child1 = child1[k]
                                    small_child2 = child2[k]

                                    pnode = Product(children=[Copy(small_child1), Copy(small_child2)])
                                    rebuild_scopes_bottom_up(pnode)
                                    sublayer.append(pnode)
                                    if k == 2:
                                        break
                layer.append(sublayer)
            spfflow_layers.append(layer)
        if i % 2 == 0 and i != 0:
            layer = []
            for j in range(len(spn.layers[i])):
                sublayer = []
                for k in range(spn.num_sums):
                    children = spfflow_layers[i - 1][j]
                    snode = Sum(weights=[1/len(children) for k in range(len(children))], children=children)
                    rebuild_scopes_bottom_up(snode)
                    sublayer.append(snode)
                layer.append(sublayer)
            spfflow_layers.append(layer)

    children = [sublist[0] for sublist in spfflow_layers[-1]]
    new_spn = Sum(weights=[1/len(children) for k in range(len(children))], children=children)
    assign_ids(new_spn)
    rebuild_scopes_bottom_up(new_spn)
    #new_spn = strip_nodes(new_spn, spn)
    return new_spn

def convert_ratspn_to_spfflow(spn, leaftype=None):
    spfflow_layers = []
    for i in range(len(spn.layers) - 1):
        if i == 0:
            layer = []
            for nodes in spn.region_graph_layers[i]:
                sublayer = []
                for j in range(spn.num_input_distributions):
                    subsublayer = []
                    for scope in range(len(nodes)):
                        if leaftype == Bernoulli:
                            subsublayer.append(Bernoulli(p=0.1, scope=int(nodes[scope])))
                        else:
                            subsublayer.append(Gaussian(mean=0.1, stdev=0.1, scope=int(nodes[scope])))
                    sublayer.append(subsublayer)
                layer.append(sublayer)
            spfflow_layers.append(layer)
        if i == 1:
            layer = []
            for j in range(len(spn.layers[i])):
                sublayer = []
                child1_layer, child2_layer = extract_number(spn.layers[i][j].name)
                for child1 in (spfflow_layers[i - 1][child1_layer]):
                    for child2 in (spfflow_layers[i - 1][child2_layer]):
                        copy = [Copy(j) for j in child1 + child2]
                        pnode = Product(children=copy)
                        rebuild_scopes_bottom_up(pnode)
                        sublayer.append(pnode)
                layer.append(sublayer)
            spfflow_layers.append(layer)

        if i % 2 != 0 and i != 1:
            layer = []
            for j in range(len(spn.layers[i])):
                sublayer = []
                child1_layer, child2_layer = extract_number(spn.layers[i][j].name)
                for child1 in spfflow_layers[i - 1]:
                    # print(spn.region_graph_layers[i-1][child1_layer])
                    if set(child1[0].scope) == set(list(spn.region_graph_layers[i - 1][child1_layer])):
                        # child1_unsorted_layer = child1
                        for child2 in spfflow_layers[i - 1]:
                            if set(child2[0].scope) == set(list(spn.region_graph_layers[i - 1][child2_layer])):
                                # child2_unsorted_layer = child2
                                for small_child1 in child1:
                                    for small_child2 in child2:
                                        pnode = Product(children=[Copy(small_child1), Copy(small_child2)])
                                        rebuild_scopes_bottom_up(pnode)
                                        sublayer.append(pnode)
                layer.append(sublayer)
            spfflow_layers.append(layer)
        if i % 2 == 0 and i != 0:
            layer = []
            for j in range(len(spn.layers[i])):
                sublayer = []
                for k in range(spn.num_sums):
                    children = spfflow_layers[i - 1][j]
                    snode = Sum(weights=[1 / len(children) for i in range(len(children))], children=children)
                    rebuild_scopes_bottom_up(snode)
                    sublayer.append(snode)
                layer.append(sublayer)
            spfflow_layers.append(layer)

    children = [item for sublist in spfflow_layers[-1] for item in sublist]
    new_spn = Sum(weights=[1 / len(children) for k in range(len(children))], children=children)
    assign_ids(new_spn)
    rebuild_scopes_bottom_up(new_spn)
    return new_spn





