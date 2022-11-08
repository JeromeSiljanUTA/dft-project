"""
dft takes audio files and figures out what button was pressed
"""

import os
import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import read
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks


def graph():
    plt.cla()
    peak_y = [y[peak] for peak in peaks]

    index = peak_y.index(max(peak_y))
    first = (peaks[index], peak_y[index])
    peaks.pop(index)
    peak_y.pop(index)

    index = peak_y.index(max(peak_y))
    second = (peaks[index], peak_y[index])
    peaks.pop(index)
    peak_y.pop(index)

    plt.scatter(*first, color="green")
    plt.scatter(*second, color="green")

    # plt.scatter(peaks, peak_y, color="orange")
    plt.plot(wave, color="blue")
    plt.show()


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
