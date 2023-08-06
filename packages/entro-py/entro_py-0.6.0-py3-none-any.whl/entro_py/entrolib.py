import math
"""
entrolib.py: Function library for different data entropy tests.
"""
__author__    = "Pavel Chikul"
__copyright__ = "Copyright 2018, REGLabs"


def compute_shannon(data):
    """
    Calculate Shannon entropy value for a given byte array.

    Keyword arguments:
    data -- data bytes
    """
    entropy = 0
    for x in range(256):
        it = float(data.count(x))/len(data)
        if it > 0:
            entropy += - it * math.log(it, 2)

    return entropy


def compute_monte_carlo_pi(data):
    """
    Calculate Monte Carlo Pi approximation for a given byte array.

    Keyword arguments:
    data -- data bytes
    """
    set_length = int(len(data) / 2) # All of the set values are inside square.
    r_square = 128 * 128
    circle_surface = 0

    for i in range(set_length):
        if ((data[i*2] - 128) ** 2 + (data[i*2+1] - 128) ** 2) <= r_square:
            circle_surface += 1

    return 4 * circle_surface / set_length


def get_pi_deviation(pi_value):
    """
    Returns an absolute percentage of difference between the provided Pi value and canonic.

    Keyword arguments:
    pi_value -- Pi value to be tested for difference
    """
    return abs(100 - (pi_value * 100 / math.pi))


def compute_chi_squared(data):
    """
    Calculate Chi-Squared value for a given byte array.

    Keyword arguments:
    data -- data bytes
    """
    if len(data) == 0:
        return 0

    expected = float(len(data)) / 256.
    observed = [0] * 256
    for b in data:
        observed[b] += 1

    chi_squared = 0
    for o in observed:
        chi_squared += (o - expected) ** 2 / expected

    return chi_squared


def compute_arithmetic_mean(data):
    """
    Calculate arithmetic mean value for a given byte array. In a truly random data blob 
    the result of arithmetic mean should lay around value of 127.5

    Keyword arguments:
    data -- data bytes
    """
    return sum(data) / float(len(data))


def compute_entropy_graph(data, step, shannon=True, chi=True, mean=True):
    """
    Calculates entropy graph values with different with different algorithms and step.

    Keyword arguments:
    data -- data bytes
    step -- step in bytes
    shannon -- indicates whether Shannon entropy should be calculated
    chi -- indicates whether Chi-Squared should be calculated
    """
    shannons = []
    chis = []
    means = []
    current_position = 0

    while current_position < len(data):
        if shannon:
            shannons.append(compute_shannon(data[current_position:current_position + step]))

        if chi:
            chis.append(compute_chi_squared(data[current_position:current_position + step]))

        if mean:
            means.append(compute_arithmetic_mean(data[current_position:current_position + step]))

        current_position += step # Note: We skip the last chunk if it's less than step.

    return (shannons, chis, means)
