import numpy as np
import matplotlib.pyplot as plt
from utils.imutil import imshow

# expects output directly from librosa.stft or librosa.cqt
def specshow(x, sr=44100, hop_length=512, max_frames=1960, skip=1, gamma=6, use_mag=True, cmap='inferno', zoom=None, show=True):
    bins, frames = x.shape
    seconds = (frames * hop_length) / sr
    minutes = int(seconds // 60)
    seconds = seconds - (minutes * 60)
    sx = x[:,:max_frames*skip:skip]
    if not np.iscomplexobj(sx):
        spec = np.copy(sx)
    else:
        mag = np.abs(sx)
        spec = mag if use_mag else np.log(1+mag**2)
    spec -= spec.min()
    spec = spec / spec.max()
    spec **= 1 / gamma
    cm = plt.get_cmap(cmap)
    spec = cm(spec)[:,:,:3]
    img = 255 * np.flipud(spec)
    if show:
        imshow(img, retina=zoom is None, zoom=zoom)
        print(f'{minutes}:{seconds:04.2f} @ {sr}Hz, {frames} frames x {bins} bins @ {hop_length} hop_length')
    else:
        return img