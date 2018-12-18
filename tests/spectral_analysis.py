import numpy as np
import matplotlib.pyplot as plt
import detect
import scipy.io.wavfile as wavutils
import windows

if __name__ == '__main__':
    test_dir = 'resources/test_set/'
    test_filename = 'wrecking_ball.wav'

    srate, data = wavutils.read(test_dir + test_filename)

    notes, chunks = detect.detect_notes(data, srate)

    start, end = 0, 0
    for i in range(len(notes)):
        if notes[i] == ("C", 6):
            start = chunks[i][0]
            end = chunks[i][1]


    t = data[start:(end + 1)]
    wlen = end - start + 1
    f = np.fft.fft(t * windows.han(wlen), wlen)
    f = np.abs(f[0:round(wlen/2)])
    freq_spect = np.fft.fftfreq(wlen, 1.0/srate)
    freq_spect = freq_spect[0:round(len(freq_spect)/2)]

    plt.plot(freq_spect, f)
    plt.show()

