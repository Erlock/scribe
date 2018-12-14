import math

A = 440.0

half_step = 2**(1.0/12)

NOTES = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

def closest_note(freq):
    try:
        n = round(math.log(freq / A, half_step))

        index = n % 12

        return NOTES[index], 4 + round(n / 12) + (index > 2)
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
