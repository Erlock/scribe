import numpy as np
import matplotlib.pyplot as plt
import detect
import scipy.io.wavfile as wavutils
import windows
import note
import sys


def get_list_of_note_indices(freq_bin, threshold=2.5e5):
    pitches = dict()

    for freq, amp in freq_bin:
        p = note.closest_note(freq)
        pitches[p] = pitches.get(p, 0) + amp

    for pitch, amp in pitches:
        if amp < threshold:
            pitches.pop(pitch)

    result = list(pitches.keys())[0]

    return result, note.freq_by_note(note), pitches[amp], 0.

    # indices = list()
    # for i in range(len(freq_bin) - 1):
    #     if freq_bin[i + 1] > threshold:
    #         indices.append(i + 1)
    # return indices

def get_base_frequency(freq_bin, threshold=2.5e5):

    freqs = list()
    amps = list()

    for freq, amp in freq_bin:
        if amp > threshold:
            freqs.append(freq)
            amps.append(amp)

    notes = [note.closest_note(x) for x in freqs]

    note_bin = list()

    weights = dict()

    for i, n in enumerate(notes):
        if n not in note_bin:
            note_bin.append(n)
            weights[n] = 0.
        weights[n] += amps[i]

    base = note_bin[0]
    best_match = 0

    total_energy = np.sum(amps)

    for base_candidate, octave in note_bin:
        harmonics = note.generate_harmonics(base_candidate, octave)

        harm_match = 0
        harm_count = 0

        for harm in harmonics:
            if harm in note_bin:
                harm_match += weights[harm]
                harm_count += 1

        spect_match = harm_count / len(note_bin)
        harm_match = harm_match / total_energy
        score = spect_match * harm_match

        if score > best_match:
            best_match = score
            base = base_candidate, octave

    index = note_bin.index(base)

    return base, freqs[index], amps[index], score


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
