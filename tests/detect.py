import scipy.io.wavfile as wavutils
import numpy as np
import matplotlib.pyplot as plt
import note
import wavgen
import windows

THRESHOLD = 5
MISMATCHES = 5

CHUNKS = [
        ( 0.020,  0.363), ( 0.413,  0.765), ( 0.809,  1.165),
        ( 1.208,  1.564), ( 1.610,  1.963), ( 2.009,  2.361),
        ( 2.411,  2.762), ( 2.809,  3.159), ( 3.210,  4.362),
        ( 4.408,  4.759), ( 4.805,  5.161), ( 5.208,  5.561),
        ( 5.607,  6.764), ( 6.808,  7.162), ( 7.211,  7.560),
        ( 7.608,  7.959), ( 8.010,  9.160), ( 9.207,  9.561),
        ( 9.608,  9.964), (10.009, 10.362), (10.409, 10.762),
        (10.808, 11.164), (11.210, 11.562), (11.609, 11.961),
        (12.009, 12.264), (12.408, 12.760), (12.809, 13.961),
        (14.008, 14.384)
        ]

test_dir = 'resources/test_set/'
test_filename = 'fur_elise.wav'

srate, data = wavutils.read(test_dir + test_filename)

print(f'Testing for: {test_filename}')

slen = len(data)

i = 0
spect = list()
freqs = list()

for start,end in CHUNKS:
    start = int(start * srate)
    end = int(end * srate)
    t = data[start:(end + 1)]
    wlen = end - start + 1
    f = np.fft.fft(t * windows.han(wlen), wlen)

    spect.append(np.abs(f[0:round(wlen/2)]))
    freq_spect = np.fft.fftfreq(wlen, 1.0/srate)
    freqs.append(freq_spect[0:round(len(freq_spect)/2)])


base_freqs = list()
for i in range(len(spect)):
    base_freqs.append(freqs[i][np.argmax(spect[i])])

notes = [note.closest_note(i) for i in base_freqs]

print(notes)

song = np.array([])
prev_chunk = (0.0, 0.0)
for i in range(len(notes)):
    freq = note.freq_by_note(notes[i][0], notes[i][1])
    song = np.append(song, np.zeros(round(CHUNKS[i][0] - prev_chunk[1])*
        srate))
    song = np.append(song, wavgen.sine_wave(freq, round((CHUNKS[i][1] -
        CHUNKS[i][0]) * srate), srate))
    prev_chunk = CHUNKS[i]

wavutils.write('result.wav', srate, song)
