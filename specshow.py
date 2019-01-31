import numpy as np
import matplotlib.pyplot as plt
from utils.imutil import imshow

def specshow(x, spacing=256, sr=44100, max_frames=1960, skip=1, gamma=6, use_mag=True, cmap='inferno'):
    frames, bins = x.shape
    seconds = (frames * spacing) / sr
    minutes = int(seconds // 60)
    seconds = seconds - (minutes * 60)
    sx = x[:max_frames*skip:skip]
    if not np.iscomplexobj(sx):
        spec = np.copy(sx)
    else:
        mag = np.abs(sx)
        spec = mag if use_mag else np.log(1+mag**2)
    spec -= spec.min()
    spec = spec.T / spec.max()
    spec **= 1 / gamma
    cm = plt.get_cmap(cmap)
    spec = cm(spec)[:,:,:3]
    imshow(255 * np.flipud(spec), retina=True)
    print(f'{minutes}:{seconds:04.2f} @ {sr}Hz, {frames} frames x {bins} bins @ {spacing} spacing')
