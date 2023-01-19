from persist import read_spn_from_equationFile, write_spn_as_equationFile
from spn.structure.leaves.parametric.Parametric import Categorical, Gaussian

from spn.structure.Base import Sum, Product
from spn.structure.Base import assign_ids, rebuild_scopes_bottom_up


def example_spn_from_spn():

    p0 = Product(
        children=[
            Categorical(p=[0.3, 0.7], scope=1),
            Categorical(p=[0.4, 0.6], scope=2),
        ]
    )
    p1 = Product(
        children=[
            Categorical(p=[0.5, 0.5], scope=1),
            Categorical(p=[0.6, 0.4], scope=2),
        ]
    )
    s1 = Sum(weights=[0.3, 0.7], children=[p0, p1])
    p2 = Product(children=[Categorical(p=[0.2, 0.8], scope=0), s1])
    p3 = Product(
        children=[
            Categorical(p=[0.2, 0.8], scope=0),
            Categorical(p=[0.3, 0.7], scope=1),
        ]
    )
    p4 = Product(children=[p3, Categorical(p=[0.4, 0.6], scope=2)])
    spn = Sum(weights=[0.4, 0.6], children=[p2, p4])

    assign_ids(spn)
    rebuild_scopes_bottom_up(spn)
    return spn


def example_spn_from_paper_about_spn():
    # scope 0 = a
    a = Categorical(p=[0.0, 1.0], scope=0)
    a_not = Categorical(p=[1.0, 0.0], scope=0)

    # scope 1 = b
    b = Categorical(p=[0.0, 1.0], scope=1)
    b_not = Categorical(p=[1.0, 0.0], scope=1)

    # scope 2 = c
    c = Categorical(p=[0.0, 1.0], scope=2)
    c_not = Categorical(p=[1.0, 0.0], scope=2)

    n_14 = Sum(weights=[0.1, 0.9], children=[c, c_not])  # 0.1, 0.9
    n_15 = Sum(weights=[0.8, 0.2], children=[c, c_not])
    n_16 = Sum(weights=[0.3, 0.7], children=[c, c_not])

    n_8 = Product(children=[n_14, b])
    n_9 = Product(children=[n_15, b_not])
    n_10 = Product(children=[b, n_16])
    n_11 = Product(children=[b_not, n_16])

    n_6 = Sum(weights=[0.4, 0.6], children=[n_8, n_9])
    n_7 = Sum(weights=[0.5, 0.5], children=[n_10, n_11])

    n_2 = Product(children=[a, n_6])
    n_3 = Product(children=[n_7, a_not])

    n_1 = Sum(weights=[0.3, 0.7], children=[n_2, n_3])

    spn = n_1

    assign_ids(spn)
    rebuild_scopes_bottom_up(spn)

    from spn.io.Text import spn_to_str_equation
    from spn.io.Text import str_to_spn

    spn_str = spn_to_str_equation(spn)
    spn = str_to_spn(spn_str)

    return spn


def example_spn_from_paper_about_spn_with_gaussian():
    # scope 0 = a
    # a = Categorical(p=[0.0, 1.0], scope=0)
    # a_not = Categorical(p=[1.0, 0.0], scope=0)
    a = Gaussian(mean=0.0, stdev=2.2, scope=0)
    a_not = Gaussian(mean=0.0, stdev=2.2, scope=0)

    # scope 1 = b
    b = Categorical(p=[0.0, 1.0], scope=1)
    b_not = Categorical(p=[1.0, 0.0], scope=1)

    # scope 2 = c
    c = Categorical(p=[0.0, 1.0], scope=2)
    c_not = Categorical(p=[1.0, 0.0], scope=2)

    n_14 = Sum(weights=[0.1, 0.9], children=[c, c_not])  # 0.1, 0.9
    n_15 = Sum(weights=[0.8, 0.2], children=[c, c_not])
    n_16 = Sum(weights=[0.3, 0.7], children=[c, c_not])

    n_8 = Product(children=[n_14, b])
    n_9 = Product(children=[n_15, b_not])
    n_10 = Product(children=[b, n_16])
    n_11 = Product(children=[b_not, n_16])

    n_6 = Sum(weights=[0.4, 0.6], children=[n_8, n_9])
    n_7 = Sum(weights=[0.5, 0.5], children=[n_10, n_11])

    n_2 = Product(children=[a, n_6])
    n_3 = Product(children=[n_7, a_not])

    n_1 = Sum(weights=[0.3, 0.7], children=[n_2, n_3])

    spn = n_1

    assign_ids(spn)
    rebuild_scopes_bottom_up(spn)

    from spn.io.Text import spn_to_str_equation
    from spn.io.Text import str_to_spn

    spn_str = spn_to_str_equation(spn)
    spn = str_to_spn(spn_str)

    return spn


from spn.io.Text import spn_to_str_equation


# my_spn = example_spn_from_paper_about_spn_with_gaussian()
# str_spn = spn_to_str_equation(my_spn)
# f = open("./spn_with_gaussian.in", "w")
# f.write(str_spn)

# https://github.com/SPFlow/SPFlow/blob/master/src/spn/experiments/layers/mnist_test.py
def example_spn_mnist():
    # from spn.experiments.layers.mnist_test import get_mnist_spn

    # spn = get_mnist_spn(200)[2]
    # write_spn_as_equationFile(spn, "mnist_spn.eq")
    return read_spn_from_equationFile("mnist_spn.eq")


# example_spn_mnist()


# from spn.io.Graphics import plot_spn
# plot_spn(spn_mnist, "plots/mnist_plot.png")
