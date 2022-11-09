"""
dft.py takes a wav file of DTMF presses, runs them through a DFT and identifies the key pressed.
"""

# imports
import os

import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.io.wavfile import read
from scipy.signal import find_peaks


def identify(maxima):
    """Takes maxima as an argument and finds the closest recognized frequency.

    Parameters:
    maxima: list of x values of two highest peaks (two most promiment frequencies)

    Returns: 
    keypad value that corresponds with key pressed"""

    low_freqs = np.array([697, 770, 852, 941])
    high_freqs = np.array([1209, 1336, 1477, 1633])
    close_low = low_freqs[(np.abs(low_freqs - maxima[0])).argmin()]
    close_high = high_freqs[(np.abs(high_freqs - maxima[1])).argmin()]

    return keypad[(close_low, close_high)]


def find_maxima(y_vals, peaks):
    """Finds the two frequencies that make up the beep.

    Takes y_vals and peaks (x values of maxima) and picks two largest values.

    Parameters:
    y_vals: values of peaks identified
    peaks: x values (frequencies) of peaks in DFT

    Returns:
    x values of highest peaks.

    """
    peak_y = [y_vals[peak] for peak in peaks]

    arr = [0, 0]
    for idx in range(2):
        index = peak_y.index(max(peak_y))
        arr[idx] = peaks[index]
        peaks.pop(index)
        peak_y.pop(index)

    return [min(arr), max(arr)]


def main():
    """Decodes wav file"""
    for sound in sounds:
        sampling_rate, in_wave = read(f"project data/{sound}")
        wave_size = in_wave.size

        wave = [
            np.abs(i)
            for i in zip(fftfreq(wave_size, 1 / sampling_rate), fft(in_wave))
            if i[0] > 0
        ]
        _, y_vals = zip(*wave)

        peaks, _ = find_peaks(y_vals)
        peaks = list(peaks)
        maxima = find_maxima(y_vals, peaks)
        result = identify(maxima)
        print(f"{sound} is {result}")


sounds = os.listdir("project data")

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

if __name__ == "__main__":
    main()
