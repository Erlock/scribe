import os
import sys, getopt
import detect
import scipy.io.wavfile as wavutils

def print_separator():
    print('-------------------------------')


if __name__ == "__main__":
    args = sys.argv

    input_dir = 'resources/test_set/'
    output_dir = 'results/'

    if len(args) == 2 or len(args) > 4:
        print('Usage: make run <input_dir> <output_dir>')
        quit()
    if len(args) == 3:
        input_dir = args[1]
        output_dir = args[2]

    for filename in os.listdir(input_dir):
        print_separator()
        print(f'Detecting notes for {filename}:')

        srate, data = wavutils.read(input_dir + filename)

        notes, chunks = detect.detect_notes(data, srate)
        print(notes)
        detect.write_song(output_dir + filename, srate, notes, chunks)
    print_separator()
