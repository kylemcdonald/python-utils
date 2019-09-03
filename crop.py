import numpy as np

def safe_crop(arr, tblr, fill=128):
    n,s,w,e = tblr
    shape = np.asarray(arr.shape)
    shape[:2] = s - n, e - w
    no, so, wo, eo = 0, shape[0], 0, shape[1]
    if n < 0:
        no += -n
        n = 0
    if w < 0:
        wo += -w
        w = 0
    if s >= arr.shape[0]:
        so -= s - arr.shape[0]
        s = arr.shape[0]
    if e >= arr.shape[1]:
        eo -= e - arr.shape[1]
        e = arr.shape[1]
    out = np.empty(shape, dtype=arr.dtype)
    out.fill(fill)
    try:
        out[no:so,wo:eo] = arr[n:s,w:e]
    except ValueError:
        pass
    return out

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
