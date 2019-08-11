import numpy as np
import math

def find_rectangle(n): 
    max_side = int(math.sqrt(n))
    for h in range(2, max_side+1)[::-1]:
        w = n // h
        if (h * w) == n:
            return (h, w)
    return (n, 1)

def swapaxes(x,a,b):
    try:
        return x.swapaxes(a,b)
    except AttributeError: # support pytorch
        return x.transpose(a,b)

# 1d images (n, h*w): no
# 2d images (n, h, w): yes
# 3d images (n, h, w, c): yes
def make_mosaic(x, nx=None, ny=None):
    if not isinstance(x, np.ndarray):
        x = np.asarray(x)
    
    n, h, w = x.shape[:3]
    has_channels = len(x.shape) > 3
    if has_channels:
        c = x.shape[3]
        
    if nx is None and ny is None:
        ny,nx = find_rectangle(n)
    elif ny is None:
        ny = n//nx
    elif nx is None:
        nx = n//ny
        
    end_shape = (w,c) if has_channels else (w,)
    mosaic = x.reshape(ny, nx, h, *end_shape)
    mosaic = swapaxes(mosaic, 1, 2)
    hh = mosaic.shape[0] * mosaic.shape[1]
    ww = mosaic.shape[2] * mosaic.shape[3]
    end_shape = (ww,c) if has_channels else (ww,)
    mosaic = mosaic.reshape(hh, *end_shape)
    return mosaic

# 1d images (n, h*w): no
# 2d images (n, h, w): yes
# 3d images (n, h, w, c): yes
# assumes images are square if underspecified
def unmake_mosaic(mosaic, nx=None, ny=None, w=None, h=None):
    hh, ww = mosaic.shape[:2]
    
    if nx is not None or ny is not None:
        if nx is None:
            h = hh//ny
            w = h
            nx = ww//w
        elif ny is None:
            w = ww//nx
            h = w
            ny = hh//h
        else:
            w = ww//nx
            h = hh//ny
        
    elif w is not None or h is not None:
        if w is None:
            w = h
        elif h is None:
            h = w
        nx = ww//w
        ny = hh//h
    
    end_shape = (w, mosaic.shape[2]) if len(mosaic.shape) > 2 else (w,)

    x = mosaic.reshape(ny, h, nx, *end_shape)
    x = swapaxes(x, 1, 2)
    x = x.reshape(-1, h, *end_shape)
    return x