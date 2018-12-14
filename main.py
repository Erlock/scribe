import scipy.io.wavfile as wavutils
import numpy as np
import matplotlib.pyplot as plt
import note
import wavgen
import os

THRESHOLD = 5

WLEN = 1000
WOVERLAP = 10

directory = os.fsencode('resources/test_set/')

MAX_TESTS = 2

figure, ax = plt.subplots(min(MAX_TESTS, len(os.listdir(directory))))

test_count = 0

for osfile in os.listdir(directory):

    if test_count >= MAX_TESTS:
        break

    filename = os.fsdecode(osfile)

    SRATE, data = wavutils.read(f'resources/test_set/{filename}')
    print(filename)

    SLEN = len(data)

    i = 0
    spect = list()
    centres = list()
    while i + WLEN <= SLEN:
        t = data[i:(i+WLEN)]
        f = np.fft.fft(t)

        spect.append(np.abs(f[0:len(f)//2]))
        centres.append((i + WLEN)/2)

        i += WLEN - WOVERLAP

    centres = np.array(centres)

    notes = [note.closest_note(np.argmax(f) * SRATE / WLEN) for f in spect if
            np.argmax(f) > 0]

    i = 0
    collapsed_notes = list()
    coll_note_count = list()
    while i < len(notes):
        j = i + 1
        while j < len(notes) and (notes[i][0] == notes[j][0]):
            j += 1;
        if j - i > THRESHOLD:
            collapsed_notes.append(notes[i])
            coll_note_count.append(j-i)
        i = j

    print(collapsed_notes)

    song = np.array([])

    for i in range(len(collapsed_notes)):
        freq = note.freq_by_note(collapsed_notes[i][0], collapsed_notes[i][1])
        song = np.append(song, wavgen.sine_wave(freq, coll_note_count[i] * WLEN, SRATE))

    name = filename.split('.')

    wavutils.write(f'resources/results/{name[0]}_result.wav', SRATE, song)

    ax[test_count].imshow(np.flipud(np.swapaxes(np.log(np.array(spect)), 0, 1)), aspect="auto", extent=[0,
        centres[len(centres)-1], 0, SRATE//2])
    ax[test_count].set_title(name[0])

    test_count += 1

plt.show()
