import scipy.io.wavfile as wavutils
import numpy as np
import matplotlib.pyplot as plt


def filter_signal(data, threshold=250):
    cpdata = np.copy(data)
    cpdata.setflags(write=True)
    cpdata[np.logical_and((cpdata <= threshold), (cpdata >= -threshold))] = 0
    return cpdata


def get_onsets(data, srate, c=2):
    i = 0
    onsets = list()
    while i < len(data):
        while i < len(data) and data[i] == 0:
            i += 1
        if i >= len(data):
            break
        j = i + 1
        empties = 0
        while j < len(data) and empties <= c:
            if data[j] == 0:
                empties += 1
            else:
                empties = 0
            j += 1
        if data[i] != 0:
            if empties > c:
                onsets.append((i, (j - c)))
            elif j >= len(data):
                onsets.append((i, len(data) - 1))
        i = j
    return onsets


if __name__ == "__main__":

    test_dir = "resources/test_set/"
    test_filename = "te_deum.wav"

    srate, data = wavutils.read(test_dir + test_filename)

    figure, ax = plt.subplots(2)
    ax[0].plot(data)

    print(f"Starting onset detection for {test_filename}")
    filtered_data = filter_signal(data)
    chunks = get_onsets(filtered_data, srate, 1000)

    indices = np.ones(len(data), dtype=bool)

    for i in range(len(chunks)):
        for j in range(chunks[i][0], chunks[i][1]):
            indices[j] = False

    cpdata = data
    cpdata.setflags(write=True)
    cpdata[indices] = 0

    ax[1].plot(cpdata)
    plt.show()
