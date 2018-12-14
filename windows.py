import numpy as np

def sinusoidal(wlen, power=2):
    return np.array([np.sin(np.pi*x/wlen)**power for x in range(wlen)])

def square(wlen):
    return np.ones(wlen)
