import os.path
import src.max_no_detect as scribe
import numpy as np
import matplotlib.pyplot as plt

PATH = 'resources/test_set/recorder/'
SOL_PATH = 'resources/solutions/recorder.txt'


def change_wlen(solutions, filelist):
    print(f'Varying wlen')
    total = len(solutions)
    wlens = np.linspace(500, 5000, num=20, dtype=int)
    matches = list()
    for wlen in wlens:
        count = 0
        num_notes = 0
        for f in filelist:
            num_notes += len(solutions[f])
            m = 0
            result = scribe.transcribe(PATH + f, wlen=wlen)
            # if solutions[f] == result:
            #     count += 1
            for x, y in zip(solutions[f], result):
                if x == y:
                    count += 1

        count /= num_notes
        matches.append(count)

    print(wlens)
    print(matches)
    plt.plot(wlens, matches)
    plt.xticks(wlens)
    plt.show()

def change_mismatches(solutions, filelist):
    print(f'Varying mismatches')
    total = len(solutions)
    mismatches = range(0, 15)
    matches = list()
    for mismatch in mismatches:
        count = 0
        num_notes = 0
        for f in filelist:
            num_notes += len(solutions[f])
            m = 0
            result = scribe.transcribe(PATH + f, mismatches=mismatch)
            # if solutions[f] == result:
            #     count += 1
            for x, y in zip(solutions[f], result):
                if x == y:
                    count += 1

        count /= num_notes
        matches.append(count)

    print(mismatches)
    print(matches)
    plt.plot(mismatches, matches)
    plt.xticks(mismatches)
    plt.show()

def change_threshold(solutions, filelist):
    print(f'Varying threshold')
    total = len(solutions)
    thresholds = range(50, 500, 50)
    matches = list()
    for threshold in thresholds:
        print(f'Threshold value {threshold}')
        count = 0
        num_notes = 0
        for f in filelist:
            num_notes += len(solutions[f])
            m = 0
            result = scribe.transcribe(PATH + f, threshold=threshold)
            # if solutions[f] == result:
            #     count += 1
            for x, y in zip(solutions[f], result):
                if x == y:
                    count += 1

        count /= num_notes
        matches.append(count)

    print(thresholds)
    print(matches)
    plt.plot(thresholds, matches)
    plt.xticks(thresholds)
    plt.show()

if __name__ == '__main__':
    filelist = os.listdir(PATH)
    solutions = dict()
    with open(SOL_PATH) as f:
        print('Reading solutions')
        lines = f.read().splitlines()
        names, notes = lines[::2], lines[1::2]
        for i, name in enumerate(names):
            nlist = notes[i].split(',')
            tones, octaves = nlist[::2], [int(x) for x in nlist[1::2]]
            solutions[name] = list(zip(tones, octaves))

    # change_wlen(solutions, filelist)
    # change_mismatches(solutions, filelist)
    change_threshold(solutions, filelist)
