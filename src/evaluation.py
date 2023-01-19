from spn.algorithms.Inference import likelihood
from spn.structure.Base import Sum, Product
import numpy as np

used_edges = {}

from spn.structure.Base import get_nodes_by_type
from spn.structure.leaves.parametric.Parametric import Categorical


class Evaluation:
    def __init__(self, spn_root) -> None:
        self.__spn = spn_root
        self.__node_likelihood = {
            Sum: self.__sum_likelihood,
            Product: self.__prod_likelihood,
            Categorical: self.__categorical_likelihood,
        }
        self.__init_edge_usage()

    @property
    def used_edges(self):
        return self.__used_edges

    @property
    def spn(self):
        return self.__spn

    def __init_edge_usage(self):
        self.__used_edges = {}
        for sumNode in get_nodes_by_type(self.spn, ntype=Sum):
            for child in sumNode.children:
                self.__used_edges[(sumNode.id, child.id)] = 0

    def __count_edge_usage(self, sumNode, childProductNode):
        currentAmount = self.__used_edges.get((sumNode.id, childProductNode.id))
        if currentAmount == None:
            currentAmount = 0
        currentAmount += 1
        self.__used_edges[(sumNode.id, childProductNode.id)] = currentAmount

    def __sum_likelihood(self, node, children, dtype=np.float64, **kwargs):
        llchildren = np.concatenate(children, axis=1)

        for index in range(len(llchildren)):
            currentValues = llchildren[index]
            childIndexOfGreaterZero = np.where(currentValues > 0)[0][0]
            self.__count_edge_usage(node, node.children[childIndexOfGreaterZero])

        assert llchildren.dtype == dtype
        # assertion that weights sum to 1
        # assert np.isclose(
        #    np.sum(node.weights), 1.0
        # ), "unnormalized weights {} for node {}".format(node.weights, node)

        b = np.array(node.weights, dtype=dtype)
        return np.dot(llchildren, b).reshape(-1, 1)

    def __prod_likelihood(self, node, children, dtype=np.float64, **kwargs):
        llchildren = np.concatenate(children, axis=1)
        assert llchildren.dtype == dtype
        return np.prod(llchildren, axis=1).reshape(-1, 1)

    def __categorical_likelihood(self, node, data, dtype=np.float64, **kwargs):
        result = []
        for index in range(len(data)):
            result.append([node.p[data[index][node.scope[0]]]])
        return result

    def evaluate_edges(self, data) -> dict:
        """
        Takes the given SPN represented by the root node and counts the edge usage, only categorial leaf nodes allowed


        :param rootNode: spn root
        :param data: categorial values for the leaf nodes of the spn
        :return: a dictionary with a tuple of IDs as key and the amount of usage in the data. First ID is of the sum node, the second from the product node.
        """

        all_results = {}
        self.__init_edge_usage()
        from spn.structure.Base import eval_spn_bottom_up

        result = eval_spn_bottom_up(
            self.spn,
            self.__node_likelihood,
            all_results=all_results,
            debug=False,
            dtype=np.float64,
            data=data,
        )

        return self.__used_edges

    def evaluate_spn(self, data) -> np.float64:

        all_results = {}
        self.__init_edge_usage()
        from spn.structure.Base import eval_spn_bottom_up

        result = eval_spn_bottom_up(
            self.spn,
            self.__node_likelihood,
            all_results=all_results,
            debug=False,
            dtype=np.float64,
            data=data,
        )

        return result
