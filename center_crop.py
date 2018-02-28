import numpy as np

def center_crop(img):
    size = np.asarray(img.shape[:2])
    min_side = min(size)
    corner = np.divide(size, 2).astype(int) - (min_side // 2)
    return img[corner[0]:corner[0]+min_side, corner[1]:corner[1]+min_side]