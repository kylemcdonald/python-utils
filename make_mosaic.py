import numpy as np
import math

def find_rectangle(n): 
    max_side = int(math.sqrt(n))
    for h in range(2, max_side+1)[::-1]:
        w = n // h
        if (w * h) == n:
            return (w,h)
    return (n, 1)

# should work for 1d and 2d images, assumes images are square but can be overriden
def make_mosaic(images, n=None, nx=None, ny=None, w=None, h=None):
    if n is None and nx is None and ny is None:
        nx, ny = find_rectangle(len(images))
    else:
        nx = n if nx is None else nx
        ny = n if ny is None else ny
    images = np.array(images)
    if images.ndim == 2:
        side = int(np.sqrt(len(images[0])))
        h = side if h is None else h
        w = side if w is None else w
        images = images.reshape(-1, h, w)
    else:
        h = images.shape[1]
        w = images.shape[2]
    nx = int(nx)
    ny = int(ny)
    h = int(h)
    w = int(w)
    image_gen = iter(images)
    # should replace this code with https://stackoverflow.com/a/42041135/940196
    if len(images.shape) > 3:
        mosaic = np.empty((h*ny, w*nx, images.shape[3]))
    else:
        mosaic = np.empty((h*ny, w*nx))
    for i in range(ny):
        ia = (i)*h
        ib = (i+1)*h
        for j in range(nx):
            ja = j*w
            jb = (j+1)*w
            mosaic[ia:ib, ja:jb] = next(image_gen)
    return mosaic