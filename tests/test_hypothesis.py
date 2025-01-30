import numpy as np
import pytest

from pycircstat2 import Circular, load_data
from pycircstat2.distributions import vonmises
from pycircstat2.hypothesis import (
    V_test,
    batschelet_test,
    binomial_test,
    change_point_test,
    chisquare_test,
    circ_range_test,
    concentration_test,
    kuiper_test,
    omnibus_test,
    one_sample_test,
    rao_homogeneity_test,  # Import from PyCircStat2
    rao_spacing_test,
    rayleigh_test,
    symmetry_test,
    wallraff_test,
    watson_test,
    watson_u2_test,
    watson_williams_test,
    wheeler_watson_test,
)


def test_rayleigh_test():

    # Ch27 Example 1 (Zar, 2010, P667)
    # Using data from Ch26 Example 2.
    data_zar_ex2_ch26 = load_data("D1", source="zar")
    circ_zar_ex1_ch27 = Circular(data=data_zar_ex2_ch26["θ"].values)

    # computed directly from r and n
    result = rayleigh_test(n=circ_zar_ex1_ch27.n, r=circ_zar_ex1_ch27.r)
    np.testing.assert_approx_equal(result.z, 5.448, significant=3)
    assert 0.001 < result.pval < 0.002

    # computed directly from alpha
    result = rayleigh_test(alpha=circ_zar_ex1_ch27.alpha)
    np.testing.assert_approx_equal(result.z, 5.448, significant=3)
    assert 0.001 < result.pval < 0.002


def test_V_test():

    # Ch27 Example 2 (Zar, 2010, P669)
    data_zar_ex2_ch27 = load_data("D7", source="zar")
    circ_zar_ex2_ch27 = Circular(data=data_zar_ex2_ch27["θ"].values)

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
    data_zar_ex2_ch27 = load_data("D7", source="zar")
    circ_zar_ex3_ch27 = Circular(data=data_zar_ex2_ch27["θ"].values, unit="degree")

    # computed directly from lb and ub
    reject_null = one_sample_test(
        lb=circ_zar_ex3_ch27.mean_lb,
        ub=circ_zar_ex3_ch27.mean_ub,
        angle=np.deg2rad(90),
    )

    assert reject_null is False

    # computed directly from alpha
    reject_null = one_sample_test(alpha=circ_zar_ex3_ch27.alpha, angle=np.deg2rad(90))

    assert reject_null is False


def test_omnibus_test():

    data_zar_ex4_ch27 = load_data("D8", source="zar")
    circ_zar_ex4_ch27 = Circular(data=data_zar_ex4_ch27["θ"].values, unit="degree")

    A, pval = omnibus_test(alpha=circ_zar_ex4_ch27.alpha, scale=1)

    np.testing.assert_approx_equal(pval, 0.0043, significant=2)


def test_batschelet_test():

    data_zar_ex5_ch27 = load_data("D8", source="zar")
    circ_zar_ex5_ch27 = Circular(data=data_zar_ex5_ch27["θ"].values, unit="degree")

    C, pval = batschelet_test(
        angle=np.deg2rad(45),
        alpha=circ_zar_ex5_ch27.alpha,
    )
    np.testing.assert_equal(C, 5)
    np.testing.assert_approx_equal(pval, 0.00661, significant=3)


def test_chisquare_test():

    d2 = load_data("D2", source="zar")
    c2 = Circular(data=d2["θ"].values, w=d2["w"].values)

    result = chisquare_test(c2.w)
    np.testing.assert_approx_equal(result.chi2, 66.543, significant=3)
    assert result.pval < 0.001


def test_symmetry_test():

    data_zar_ex6_ch27 = load_data("D9", source="zar")
    circ_zar_ex6_ch27 = Circular(data=data_zar_ex6_ch27["θ"].values, unit="degree")

    d, p = symmetry_test(median=circ_zar_ex6_ch27.median, alpha=circ_zar_ex6_ch27.alpha)
    assert p > 0.5


def test_watson_williams_test():

    data = load_data("D10", source="zar")
    s1 = Circular(data=data[data["sample"] == 1]["θ"].values)
    s2 = Circular(data=data[data["sample"] == 2]["θ"].values)
    F, pval = watson_williams_test(circs=[s1, s2])

    np.testing.assert_approx_equal(F, 1.61, significant=3)
    np.testing.assert_approx_equal(pval, 0.22, significant=2)

    data = load_data("D11", source="zar")
    s1 = Circular(data=data[data["sample"] == 1]["θ"].values)
    s2 = Circular(data=data[data["sample"] == 2]["θ"].values)
    s3 = Circular(data=data[data["sample"] == 3]["θ"].values)

    F, pval = watson_williams_test(circs=[s1, s2, s3])

    np.testing.assert_approx_equal(F, 1.86, significant=3)
    np.testing.assert_approx_equal(pval, 0.19, significant=2)


def test_watson_u2_test():

    d = load_data("D12", source="zar")
    c0 = Circular(data=d[d["sample"] == 1]["θ"].values)
    c1 = Circular(data=d[d["sample"] == 2]["θ"].values)
    U2, pval = watson_u2_test(circs=[c0, c1])

    np.testing.assert_approx_equal(U2, 0.1458, significant=3)
    assert 0.1 < pval < 0.2

    d = load_data("D13", source="zar")
    c0 = Circular(
        data=d[d["sample"] == 1]["θ"].values, w=d[d["sample"] == 1]["w"].values
    )
    c1 = Circular(
        data=d[d["sample"] == 2]["θ"].values, w=d[d["sample"] == 2]["w"].values
    )
    U2, pval = watson_u2_test(circs=[c0, c1])

    np.testing.assert_approx_equal(U2, 0.0612, significant=3)
    assert pval > 0.5


def test_wheeler_watson_test():
    d = load_data("D12", source="zar")
    c0 = Circular(data=d[d["sample"] == 1]["θ"].values)
    c1 = Circular(data=d[d["sample"] == 2]["θ"].values)

    W, pval = wheeler_watson_test(circs=[c0, c1])
    np.testing.assert_approx_equal(W, 3.678, significant=3)
    assert 0.1 < pval < 0.25


def test_wallraff_test():

    d = load_data("D14", source="zar")
    c0 = Circular(data=d[d["sex"] == "male"]["θ"].values)
    c1 = Circular(data=d[d["sex"] == "female"]["θ"].values)
    U, pval = wallraff_test(angle=np.deg2rad(135), circs=[c0, c1])
    np.testing.assert_approx_equal(U, 18.5, significant=3)
    assert pval > 0.20

    from pycircstat2.utils import time2float

    d = load_data("D15", source="zar")
    c0 = Circular(data=time2float(d[d["sex"] == "male"]["time"].values))
    c1 = Circular(data=time2float(d[d["sex"] == "female"]["time"].values))
    U, pval = wallraff_test(
        angle=np.deg2rad(time2float(["7:55", "8:15"])),
        circs=[c0, c1],
        verbose=True,
    )
    np.testing.assert_equal(U, 13)
    assert pval > 0.05


def test_kuiper_test():

    d = load_data("B5", source="fisher")["θ"].values
    c = Circular(data=d, unit="degree", n_intervals=180)
    V, pval = kuiper_test(alpha=c.alpha)
    np.testing.assert_approx_equal(V, 1.5864, significant=3)
    assert pval > 0.05


def test_watson_test():

    pigeon = np.array([20, 135, 145, 165, 170, 200, 300, 325, 335, 350, 350, 350, 355])
    c_pigeon = Circular(data=pigeon)
    U2, pval = watson_test(alpha=c_pigeon.alpha, n_simulation=9999)
    np.testing.assert_approx_equal(U2, 0.137, significant=3)
    assert pval > 0.10


def test_rao_spacing_test():
    pigeon = np.array([20, 135, 145, 165, 170, 200, 300, 325, 335, 350, 350, 350, 355])
    c_pigeon = Circular(data=pigeon)
    U, pval = rao_spacing_test(alpha=c_pigeon.alpha, n_simulation=9999)
    np.testing.assert_approx_equal(U, 161.92308, significant=3)
    assert 0.05 < pval < 0.10

def test_circ_range_test():


    x = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.6, 36.0, 36.0, 36.0, 36.0, 36.0, 36.0, 72.0, 108.0, 108.0, 169.2, 324.0])
    range_stat, pval = circ_range_test(x)
    np.testing.assert_approx_equal(range_stat, 4.584073, significant=5)
    np.testing.assert_approx_equal(pval, 0.01701148, significant=5)


def test_binomial_test_uniform():
    """Test binomial_test with uniform circular data (should not reject H0)."""
    np.random.seed(42)
    alpha = np.random.uniform(0, 2 * np.pi, 100)  # Uniformly distributed angles
    md = np.pi  # Test median at π (should be non-significant)
    
    pval = binomial_test(alpha, md)
    
    assert 0.05 < pval < 1.0, f"Unexpected p-value for uniform data: {pval}"

def test_binomial_test_skewed():
    """Test binomial_test with a skewed circular distribution (should reject H0)."""
    np.random.seed(42)
    alpha = np.random.vonmises(mu=np.pi/4, kappa=3, size=100)  # Clustered around π/4
    md = np.pi  # Incorrect median hypothesis
    
    pval = binomial_test(alpha, md)
    
    assert pval < 0.05, f"Expected significant p-value but got {pval}"

def test_binomial_test_symmetric():
    """Test binomial_test with symmetric distribution around π (should fail to reject H0)."""
    alpha = np.array([-np.pi/4, np.pi/4, np.pi/2, -np.pi/2, np.pi])
    md = np.pi  # This should be a valid median
    
    pval = binomial_test(alpha, md)
    
    assert pval > 0.05, f"Unexpected p-value for symmetric data: {pval}"

def test_binomial_test_extreme_case():
    """Test binomial_test with all points clustered at π (extreme case)."""
    alpha = np.full(20, np.pi)  # All angles at π
    md = np.pi
    
    pval = binomial_test(alpha, md)
    
    assert np.isclose(pval, 1.0), f"Expected p-value of 1 for identical data but got {pval}"



def test_concentration_identical():
    """Test concentration_test with identical von Mises distributions (should fail to reject H0)."""
    np.random.seed(42)
    alpha1 = vonmises.rvs(mu=0, kappa=3, size=50)
    alpha2 = vonmises.rvs(mu=0, kappa=3, size=50)

    f_stat, pval = concentration_test(alpha1, alpha2)

    assert pval > 0.05, f"Unexpectedly small p-value: {pval}, should not reject H0."

def test_concentration_different():
    """Test concentration_test with different kappa values (should reject H0)."""
    np.random.seed(42)
    alpha1 = vonmises.rvs(mu=0, kappa=3, size=50)  # Higher concentration
    alpha2 = vonmises.rvs(mu=0, kappa=1, size=50)  # Lower concentration

    f_stat, pval = concentration_test(alpha1, alpha2)

    assert pval < 0.05, f"Expected small p-value, but got {pval}"

def test_concentration_high_dispersion():
    """Test concentration_test with very dispersed data (should fail to reject H0)."""
    np.random.seed(42)
    alpha1 = np.random.uniform(0, 2*np.pi, 50)  # Uniformly spread
    alpha2 = np.random.uniform(0, 2*np.pi, 50)

    f_stat, pval = concentration_test(alpha1, alpha2)

    assert pval > 0.05, f"Unexpectedly small p-value: {pval}, should not reject H0."


def test_concentration_extreme_case():
    """Test concentration_test when both samples have extremely high concentration (should fail to reject H0)."""
    np.random.seed(42)
    alpha1 = vonmises.rvs(mu=0, kappa=100, size=50)
    alpha2 = vonmises.rvs(mu=0, kappa=100, size=50)

    f_stat, pval = concentration_test(alpha1, alpha2)

    assert pval > 0.05, f"Unexpectedly small p-value: {pval}, should not reject H0."



def test_rao_homogeneity_identical():
    """Test with identical von Mises distributions (should fail to reject H0)."""
    np.random.seed(42)
    samples = [vonmises.rvs(mu=0, kappa=2, size=50) for _ in range(3)]

    results = rao_homogeneity_test(samples)

    assert results["pval_polar"] > 0.05, f"Unexpectedly small p-value: {results['pval_polar']}"
    assert results["pval_disp"] > 0.05, f"Unexpectedly small p-value: {results['pval_disp']}"

def test_rao_homogeneity_different_means():
    """Test with different mean directions (should reject H0 for mean equality)."""
    np.random.seed(42)
    samples = [
        vonmises.rvs(kappa=2, mu=0, size=50),
        vonmises.rvs(kappa=2, mu=np.pi/4, size=50),
        vonmises.rvs(kappa=2, mu=np.pi/2, size=50)
    ]
    results = rao_homogeneity_test(samples)

    assert results["pval_polar"] < 0.05, f"Expected rejection but got p={results['pval_polar']}"

def test_rao_homogeneity_different_dispersion():
    """Test with different kappa values (should reject H0 for dispersion equality)."""
    np.random.seed(42)
    samples = [
        vonmises.rvs(mu=0, kappa=5, size=50),
        vonmises.rvs(mu=0, kappa=2, size=50),
        vonmises.rvs(mu=0, kappa=1, size=50)
    ]

    results = rao_homogeneity_test(samples)

    assert results["pval_disp"] < 0.05, f"Expected rejection but got p={results['pval_disp']}"

def test_rao_homogeneity_small_samples():
    """Test with very small sample sizes (should handle without error)."""
    np.random.seed(42)
    samples = [vonmises.rvs(mu=0, kappa=3, size=5) for _ in range(3)]

    results = rao_homogeneity_test(samples)

    assert "pval_polar" in results and "pval_disp" in results

def test_rao_homogeneity_invalid_input():
    """Test invalid input (should raise ValueError)."""
    with pytest.raises(ValueError):
        rao_homogeneity_test("invalid_input")

    with pytest.raises(ValueError):
        rao_homogeneity_test([np.array([0, np.pi/2]), "invalid_array"])

def test_change_point_basic():
    """Test change_point_test() on a simple dataset matching R."""
    alpha = np.array([3.03, 0.28, 3.90, 5.56, 5.77, 5.06, 5.96, 
                      0.16, 0.51, 1.21, 6.03, 1.05, 0.45, 1.47, 6.09])
    
    result = change_point_test(alpha)

    # Expected values based on R output
    expected_rho = 0.52307
    expected_rmax = 2.237654
    expected_k_r = 6
    expected_rave = 1.066862
    expected_tmax = 0.602549
    expected_k_t = 6
    expected_tave = 0.460675

    assert np.isclose(result["rho"].iloc[0], expected_rho, atol=1e-5)
    assert np.isclose(result["rmax"].iloc[0], expected_rmax, atol=1e-5)
    assert result["k.r"].iloc[0] == expected_k_r
    assert np.isclose(result["rave"].iloc[0], expected_rave, atol=1e-5)
    assert np.isclose(result["tmax"].iloc[0], expected_tmax, atol=1e-5)
    assert result["k.t"].iloc[0] == expected_k_t
    assert np.isclose(result["tave"].iloc[0], expected_tave, atol=1e-5)
