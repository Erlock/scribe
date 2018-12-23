import numpy as np


def sine_wave(freq, nsamp, srate=44100):
    return np.array([np.sin(2*np.pi*freq*x/srate) for x in range(nsamp)])
