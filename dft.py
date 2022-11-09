"""
dft.py takes audio files of DTMF presses, runs them through a DFT and identifies the key pressed.
"""

# imports
import os

import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.io.wavfile import read
from scipy.signal import find_peaks


def closest(maxima):
    """identifies keypress"""

    low_freqs = np.array([697, 770, 852, 941])
    high_freqs = np.array([1209, 1336, 1477, 1633])
    close_low = low_freqs[(np.abs(low_freqs - maxima[0])).argmin()]
    close_high = high_freqs[(np.abs(high_freqs - maxima[1])).argmin()]

    keypad = {
        (697, 1209): "1",
        (697, 1336): "2",
        (697, 1477): "3",
        (697, 1633): "A",
        (770, 1209): "4",
        (770, 1336): "5",
        (770, 1477): "6",
        (770, 1633): "B",
        (852, 1209): "7",
        (852, 1336): "8",
        (852, 1477): "9",
        (852, 1633): "C",
        (941, 1209): "*",
        (941, 1336): "0",
        (941, 1477): "#",
        (941, 1633): "D",
    }
    #print(f"closest {close_low} {close_high}")
    print(f"{sound}: {maxima[0]}, {maxima[1]}: {keypad[(close_low, close_high)]}")


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
