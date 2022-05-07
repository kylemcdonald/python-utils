import numpy as np

def autrim(audio, thresh=1e-4):
    start = np.argmin(audio < thresh)
    end = np.argmax(audio[::-1] > thresh)
    return audio[start:-end-1], start, end