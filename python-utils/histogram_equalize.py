import numpy as np

def histogram_equalize(data, max_val=None, endpoint=False):
    input_shape = np.shape(data)
    data_flat = np.asarray(data).flatten()
    if max_val is None:
        max_val = data_flat.max()
    indices = np.argsort(data_flat)
    replacements = np.linspace(0, max_val, len(indices), endpoint=endpoint)
    data_flat[indices] = replacements
    return data_flat.reshape(*input_shape)