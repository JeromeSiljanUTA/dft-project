"""
dtmf
dft takes audio files and figures out what button was pressed
"""

import os
import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import read
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks


def closest(maxima):
    low_freqs = [1209, 1336, 1477, 1633]
    high_freqs = [697, 770, 852, 941]
    dist = 0
    keypad = {
        "1": [697, 1209],
        "2": [697, 1336],
        "3": [697, 1477],
        "A": [697, 1633],
        "4": [770, 1209],
        "5": [770, 1336],
        "6": [770, 1477],
        "B": [770, 1633],
        "7": [852, 1209],
        "8": [852, 1336],
        "9": [852, 1477],
        "C": [852, 1633],
        "*": [941, 1209],
        "0": [941, 1336],
        "#": [941, 1477],
        "D": [941, 1633],
    }
    print(f"{sound}: {maxima[0]}, {maxima[1]}")


def find_maxima():
    peak_y = [y[peak] for peak in peaks]

    index = peak_y.index(max(peak_y))
    first = (peaks[index], peak_y[index])
    peaks.pop(index)
    peak_y.pop(index)

    index = peak_y.index(max(peak_y))
    second = (peaks[index], peak_y[index])
    peaks.pop(index)
    peak_y.pop(index)

    arr = [first[0], second[0]]
    plt.scatter(*first, color="green")
    plt.scatter(*second, color="green")

    return [min(arr), max(arr)]


def graph():
    plt.cla()
    maxima = find_maxima()
    closest(maxima)
    plt.plot(wave, color="blue")
    # plt.show()


sounds = os.listdir("project data")

"""
calculate fourier transform, frequency bins

filter out results with an x value of < 0

get absolute value of results

store as wave
"""

for sound in sounds:
    sampling_rate, in_wave = read(f"project data/{sound}")
    n = in_wave.size

    wave = [
        np.abs(i) for i in zip(fftfreq(n, 1 / sampling_rate), fft(in_wave)) if i[0] > 0
    ]
    x, y = zip(*wave)

    # thresh_top = np.median(y) + 1 * np.std(y)
    # peaks, _ = find_peaks(y, height=thresh_top)
    peaks, _ = find_peaks(y)
    peaks = list(peaks)
    graph()
