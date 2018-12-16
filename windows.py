import numpy as np

def sinusoidal(wlen, power=2):
    return np.array([np.sin(np.pi*x/wlen)**power for x in range(wlen)])

def square(wlen):
    return np.ones(wlen)

def han(wlen):
    return np.array([0.5*(1-np.cos(2*np.pi*x/(wlen-1))) for x in range(wlen)])
