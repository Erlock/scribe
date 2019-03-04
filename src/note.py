import math

A = 440.0

half_step = 2**(1.0/12)

NOTES = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]


def closest_note(freq):
    try:
        n = round(math.log(freq / A, half_step))

        index = n % 12

        return NOTES[index], 4 + math.floor((n + 9) / 12)
    except ValueError:
        print(f'Frequency {freq} fails')


def freq_by_note(note, octave):
    try:
        index = NOTES.index(note)
    except ValueError:
        raise ValueError(f'{note} is not a valid note')

    if index > 2:
        n = (octave-5) * 12 + index
    else:
        n = (octave - 4) * 12 + index

    return A * (half_step ** n)


def get_base_freq(name):
    try:
        index = NOTES.index(name)
    except ValueError:
        raise ValueError(f'{name} is not a valid note')

    return A * (half_step ** index)
