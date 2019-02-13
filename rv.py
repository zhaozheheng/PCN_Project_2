import math

seed = 1111.0

def uni_rv():
    global seed
    k = 16807.0
    m = 2147483647.0

    seed = (k * seed) % m
    rv = seed / m
    return rv

def exp_rv(lam):
    exp = (-1.0 / lam) * math.log(uni_rv())
    return exp
