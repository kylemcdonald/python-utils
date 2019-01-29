import numpy as np

def inner_square_crop(img):
    size = np.asarray(img.shape[:2])
    min_side = min(size)
    corner = (size - min_side) // 2
    return img[corner[0]:corner[0]+min_side, corner[1]:corner[1]+min_side]

def outer_square_crop(img, fill=0):
    size = np.asarray(img.shape[:2])
    max_side = max(size)
    output_shape = np.copy(img.shape)
    output_shape[:2] = max_side
    out = np.empty(output_shape, dtype=img.dtype)
    out.fill(fill)
    corner = (max_side - size) // 2
    out[corner[0]:corner[0]+size[0], corner[1]:corner[1]+size[1]] = img
    return out
