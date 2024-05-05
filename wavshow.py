import numpy as np
import matplotlib.pyplot as plt

def wavshow(audio, sr=None, resolution=2048, plot=True):
    if len(audio.shape) == 1:
        audio = audio.reshape(-1,1)
    if audio.shape[1] > audio.shape[0]:
        audio = audio.T
    duration = len(audio)
    if sr is not None:
         duration /= sr
    plt.figure(figsize=(16,4))
    n = len(audio)
    k = n // resolution
    if k > 1:
        audio = audio[:(n//k)*k]
        audio = audio.reshape(-1,k)
        mean = audio.mean(axis=1)
        std = audio.std(axis=1)
        x_ticks = np.linspace(0, duration, audio.shape[0])
        plt.fill_between(x_ticks, mean - std, mean + std, color='black', lw=0)
        plt.fill_between(x_ticks, audio.min(axis=1), audio.max(axis=1), alpha=0.5, color='gray', lw=0)
    else:
        x_ticks = np.linspace(0, duration, len(audio))
        plt.plot(x_ticks, audio, color='black', lw=1)
    plt.xlim(0, duration)
    abs_max = np.abs(audio).max()
    plt.ylim(-abs_max, abs_max)
    plt.xlabel('Seconds' if sr is not None else 'Samples')
    if plot:
        plt.show()