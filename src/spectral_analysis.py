import numpy as np
import matplotlib.pyplot as plt
import detect
import scipy.io.wavfile as wavutils
import windows
import sys


def get_list_of_note_indices(freq_bin, threshold=2.5e5):
    indices = list()
    for i in range(len(freq_bin) - 1):
        if freq_bin[i + 1] > threshold:
            indices.append(i + 1)
    return indices


if __name__ == '__main__':
    args = sys.argv
    assert(len(args) == 4)
    test_dir = 'resources/test_set/'
    test_filename = args[1]
    note_name = args[2].upper()
    octave = int(args[3])

    srate, data = wavutils.read(test_dir + test_filename)

    notes, chunks = detect.detect_notes(data, srate)

    start, end = 0, 0
    for i in range(len(notes)):
        if notes[i] == (note_name, octave):
            start = chunks[i][0]
            end = chunks[i][1]
            break

    if end > 0:

        t = data[start:(end + 1)]
        wlen = end - start + 1
        f = np.fft.fft(t * windows.han(wlen), wlen)
        f = np.abs(f[0:round(wlen/2)])
        freq_spect = np.fft.fftfreq(wlen, 1.0/srate)
        freq_spect = freq_spect[0:round(len(freq_spect)/2)]

        plt.plot(freq_spect, f)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('FFT coefficient')
        plt.show()

    else:
        print(f'No {note_name + str(octave)} found')
