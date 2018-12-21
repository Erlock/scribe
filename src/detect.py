import scipy.io.wavfile as wavutils
import numpy as np
import matplotlib.pyplot as plt
import note
import wavgen
import windows
import time_domain
import sys
import spectral_analysis


def detect_notes(data, srate):
    i = 0
    spect = list()
    freqs = list()

    filtered_data = time_domain.filter_signal(data)
    chunks = time_domain.get_onsets(filtered_data, srate, 1000)

    for start,end in chunks:
        t = data[start:(end + 1)]
        wlen = end - start + 1
        f = np.fft.fft(t * windows.han(wlen), wlen)

        spect.append(np.abs(f[0:round(wlen/2)]))
        freq_spect = np.fft.fftfreq(wlen, 1.0/srate)
        freqs.append(freq_spect[0:round(len(freq_spect)/2)])


    base_freqs = list()
    for i in range(len(spect)):
        detected_indices = spectral_analysis.get_list_of_note_indices(spect[i],
                0.4 * np.max(spect[i]))
        base_freqs.append(freqs[i][detected_indices[0]])

    notes = [note.closest_note(i) for i in base_freqs]

    return notes, chunks

def write_song(filename, srate, notes, chunks):
    song = np.array([])
    prev_chunk = (0.0, 0.0)
    for i in range(len(notes)):
        freq = note.freq_by_note(notes[i][0], notes[i][1])
        song = np.append(song, np.zeros(round(chunks[i][0] - prev_chunk[1])))
        song = np.append(song, wavgen.sine_wave(freq, round(chunks[i][1] -
            chunks[i][0]), srate))
        prev_chunk = chunks[i]

    wavutils.write(filename, srate, song)


if __name__ == '__main__':

    args = sys.argv

    test_dir = 'resources/test_set/'
    test_filename = 'te_deum.wav'

    if len(args) > 1:
        test_filename = args[1]

    srate, data = wavutils.read(test_dir + test_filename)

    print(f'Testing for: {test_filename}')

    notes, chunks = detect_notes(data, srate)

    write_song(f'result_{test_filename}', srate, notes, chunks)
