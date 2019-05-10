import scipy.io.wavfile as wavutils
import numpy as np
import matplotlib.pyplot as plt
import src.note as note
import src.wavgen as wavgen
import src.windows as windows

import argparse
import os.path

THRESHOLD = 5
MISMATCHES = 5

WLEN = 1000
WOVERLAP = 100


def transcribe(filepath, wlen=1447, woverlap=100, threshold=100, mismatches=1, plot=False, write=False):
    filename = os.path.basename(filepath)

    srate, data = wavutils.read(filepath)

    # print(f"Testing for: {filename}")

    slen = len(data)

    i = 0
    spect = list()

    while i + wlen <= slen:
        t = data[i: (i + wlen)]
        f = np.fft.fft(t * windows.han(wlen), wlen)
        spect.append(np.abs(f[0: int(wlen / 2)]))

        i += wlen - woverlap


    freqs = np.fft.fftfreq(wlen, 1.0 / srate)
    freqs = freqs[0: round(len(freqs) / 2)]


    base_freqs = list()
    for fbin in spect:
        base_freqs.append(np.argmax(fbin))

    collapsed_freqs = list()
    counts = list()

    i = 0
    while i < len(base_freqs):
        j = i + 1
        mis = 0
        while j < len(base_freqs) and mis < mismatches:
            if base_freqs[i] == base_freqs[j]:
                mis = 0
            else:
                mis += 1
            j += 1

        last_pos = j
        if mis >= mismatches:
            last_pos = j - mis - 1

        if 1000 * wlen * (last_pos - i) / srate > threshold:
            collapsed_freqs.append(base_freqs[i])
            counts.append(last_pos - i)
        i = last_pos + 1

    notes = [note.closest_note(freqs[i]) for i in collapsed_freqs]

    if write:
        song = np.array([])
        for i in range(len(notes)):
            freq = note.freq_by_note(notes[i][0], notes[i][1])
            song = np.append(
                song[0: -(woverlap + 1)],
                wavgen.sine_wave(freq, counts[i] * wlen -
                                (counts[i] - 1) * woverlap, srate),
            )

        wavutils.write(f"results/fixed/{filename}", srate, song)

    if plot:
        plt.imshow(
            np.transpose(np.fliplr(np.log(spect))),
            aspect="auto",
            extent=[0, slen / srate, 0, freqs[len(freqs) - 1]],
        )


        plt.xlabel("Time (s)")
        plt.ylabel("Frequency (Hz)")
        plt.show()

    return notes

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', default='resources/test_set/tetris_theme.wav')
    parser.add_argument('--woverlap', type=int, default=100)
    parser.add_argument('--wlen', type=int, default=1447)
    parser.add_argument('--mismatches', type=int, default=1)
    parser.add_argument('--threshold', type=int, default=100)
    args = parser.parse_args()

    transcribe(args.input, args.wlen, args.woverlap, args.threshold, args.mismatches, plot=True, write=True)
