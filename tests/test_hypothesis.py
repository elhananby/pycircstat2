import numpy as np

from pycircstat2 import Circular, load_data
from pycircstat2.hypothesis import (
    V_test,
    batschelet_test,
    kuiper_test,
    omnibus_test,
    one_sample_test,
    rayleigh_test,
    symmetry_test,
    wallraff_test,
    watson_u2_test,
    watson_williams_test,
    wheeler_watson_test,
)


def test_rayleigh_test():

    # Ch27 Example 1 (Zar, 2010, P667)
    # Using data from Ch26 Example 2.
    data_zar_ex2_ch26 = load_data("D1", source="zar_2010")
    circ_zar_ex1_ch27 = Circular(data_zar_ex2_ch26["θ"].values)

    # computed directly from r and n
    z, p = rayleigh_test(n=circ_zar_ex1_ch27.n, r=circ_zar_ex1_ch27.r)
    np.testing.assert_approx_equal(z, 5.448, significant=3)
    assert 0.001 < p < 0.002

    # computed directly from alpha
    z, p = rayleigh_test(alpha=circ_zar_ex1_ch27.alpha)
    np.testing.assert_approx_equal(z, 5.448, significant=3)
    assert 0.001 < p < 0.002


def test_V_test():

    # Ch27 Example 2 (Zar, 2010, P669)
    data_zar_ex2_ch27 = load_data("D7", source="zar_2010")
    circ_zar_ex2_ch27 = Circular(data_zar_ex2_ch27["θ"].values)

    # computed directly from r and n
    V, u, p = V_test(
        angle=np.deg2rad(90),
        mean=circ_zar_ex2_ch27.mean,
        n=circ_zar_ex2_ch27.n,
        r=circ_zar_ex2_ch27.r,
    )

    np.testing.assert_approx_equal(V, 9.498, significant=3)
    np.testing.assert_approx_equal(u, 4.248, significant=3)
    assert p < 0.0005

    # computed directly from alpha
    V, u, p = V_test(
        alpha=circ_zar_ex2_ch27.alpha,
        angle=np.deg2rad(90),
    )

    np.testing.assert_approx_equal(V, 9.498, significant=3)
    np.testing.assert_approx_equal(u, 4.248, significant=3)
    assert p < 0.0005


def test_one_sample_test():

    # Ch27 Example 3 (Zar, 2010, P669)
    # Using data from Ch27 Example 2
    data_zar_ex2_ch27 = load_data("D7", source="zar_2010")
    circ_zar_ex3_ch27 = Circular(data=data_zar_ex2_ch27["θ"].values, unit="degree")

    # # computed directly from lb and ub
    # reject_null = one_sample_test(
    #     lb=circ_zar_ex3_ch27.mean_lb,
    #     ub=circ_zar_ex3_ch27.mean_ub,
    #     angle=90,
    #     unit="degree",
    # )

    # assert reject_null is False

    # computed directly from alpha
    reject_null = one_sample_test(alpha=circ_zar_ex3_ch27.alpha, angle=np.deg2rad(90))

    assert reject_null is False


def test_omnibus_test():

    data_zar_ex4_ch27 = load_data("D8", source="zar_2010")
    circ_zar_ex4_ch27 = Circular(data_zar_ex4_ch27["θ"].values, unit="degree")

    pval = omnibus_test(alpha=circ_zar_ex4_ch27.alpha, scale=1)

    np.testing.assert_approx_equal(pval, 0.0043, significant=2)


def test_batschelet_test():

    data_zar_ex5_ch27 = load_data("D8", source="zar_2010")
    circ_zar_ex5_ch27 = Circular(data_zar_ex5_ch27["θ"].values, unit="degree")

    pval = batschelet_test(
        angle=np.deg2rad(45),
        alpha=circ_zar_ex5_ch27.alpha,
    )
    np.testing.assert_approx_equal(pval, 0.00661, significant=3)


def test_symmetry_test():

    data_zar_ex6_ch27 = load_data("D9", source="zar_2010")
    circ_zar_ex6_ch27 = Circular(data_zar_ex6_ch27["θ"].values, unit="degree")

    p = symmetry_test(median=circ_zar_ex6_ch27.median, alpha=circ_zar_ex6_ch27.alpha)
    assert p > 0.5


def test_watson_williams_test():

    data = load_data("D10", source="zar_2010")
    s1 = Circular(data[data["sample"] == 1]["θ"].values)
    s2 = Circular(data[data["sample"] == 2]["θ"].values)
    F, pval = watson_williams_test([s1, s2])

    np.testing.assert_approx_equal(F, 1.61, significant=3)
    np.testing.assert_approx_equal(pval, 0.22, significant=2)

    data = load_data("D11", source="zar_2010")
    s1 = Circular(data[data["sample"] == 1]["θ"].values)
    s2 = Circular(data[data["sample"] == 2]["θ"].values)
    s3 = Circular(data[data["sample"] == 3]["θ"].values)

    F, pval = watson_williams_test([s1, s2, s3])

    np.testing.assert_approx_equal(F, 1.86, significant=3)
    np.testing.assert_approx_equal(pval, 0.19, significant=2)


def test_watson_u2_test():

    d = load_data("D12", source="zar_2010")
    c0 = Circular(data=d[d["sample"] == 1]["θ"].values)
    c1 = Circular(data=d[d["sample"] == 2]["θ"].values)
    U2, pval = watson_u2_test([c0, c1])

    np.testing.assert_approx_equal(U2, 0.1458, significant=3)
    assert 0.1 < pval < 0.2

    d = load_data("D13", source="zar_2010")
    c0 = Circular(
        data=d[d["sample"] == 1]["θ"].values, w=d[d["sample"] == 1]["w"].values
    )
    c1 = Circular(
        data=d[d["sample"] == 2]["θ"].values, w=d[d["sample"] == 2]["w"].values
    )
    U2, pval = watson_u2_test([c0, c1])

    np.testing.assert_approx_equal(U2, 0.0612, significant=3)
    assert pval > 0.5


def test_wheeler_watson_test():
    d = load_data("D12", source="zar_2010")
    c0 = Circular(data=d[d["sample"] == 1]["θ"].values)
    c1 = Circular(data=d[d["sample"] == 2]["θ"].values)

    W, pval = wheeler_watson_test([c0, c1])
    np.testing.assert_approx_equal(W, 3.678, significant=3)
    assert 0.1 < pval < 0.25


def test_wallraff_test():

    d = load_data("D14", source="zar_2010")
    c0 = Circular(data=d[d["sex"] == "male"]["θ"].values)
    c1 = Circular(data=d[d["sex"] == "female"]["θ"].values)
    U, pval = wallraff_test(angle=np.deg2rad(135), circs=[c0, c1])
    np.testing.assert_approx_equal(U, 18.5, significant=3)
    assert pval > 0.20


def test_kuiper_test():

    d = load_data("B5", source="fisher_1993")["θ"].values
    c = Circular(data=d, unit="degree", n_intervals=180)
    V, p = kuiper_test(c.alpha)
    np.testing.assert_approx_equal(V, 1.5864, significant=3)
