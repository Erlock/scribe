import scipy.io.wavfile as wavutils
import numpy as np
import matplotlib.pyplot as plt

def filter_signal(data, threshold=250):
    cpdata = np.copy(data)
    cpdata.setflags(write=True)
    cpdata[np.logical_and((cpdata<= threshold), (cpdata>=-threshold))] = 0
    return cpdata

def get_onsets(data, srate, c=2):
    i = 0
    onsets = list()
    while i < len(data):
        j = i + 1
        empties = 0
        while j < len(data) and empties <= c:
            if data[j] == 0:
                empties += 1
            else:
                empties = 0
            j += 1
        if empties > c and data[i] != 0:
            onsets.append((i / srate, (j - c + 1) / srate))
        while j < len(data) and data[j] == 0:
            j += 1
        i = j
    return onsets



if __name__ == '__main__':

    test_dir = 'resources/test_set/'
    test_filename = 'amazing_grace.wav'

    srate, data = wavutils.read(test_dir + test_filename)

    #plt.plot(data)

    print(f'Starting onset detection for {test_filename}')
    filtered_data = filter_signal(data)
    print(get_onsets(filtered_data, srate, 200))
    plt.plot(filtered_data)
    plt.show()
    #slen = len(data)

    #fig, ax = plt.subplots(3)

    #ax[0].plot(data)
    #ax[2].plot(data - np.roll(data, 20))

    #threshold = np.average(data[data>=0])
    #maxm = np.max(data)

    #data.setflags(write=True)
    #data[data < 0.75*maxm] = 0
    #data.setflags(write=False)


    #ax[1].plot(data)
    #plt.show()
