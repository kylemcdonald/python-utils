try: # Python 2
    from cStringIO import StringIO as BytesIO
except: # Python 3
    from io import BytesIO
import numpy as np
import PIL.Image
import IPython.display
import shutil
from math import sqrt

def show_array(img, fmt='png', filename=None, retina=False, zoom=None):
    if img is None:
        raise TypeError('input image not provided')
    
    if len(img.shape) == 1:
        n = len(img)
        side = int(sqrt(n))
        if (side * side) == n:
            img = img.reshape(side, side)
        else:
            raise ValueError('input is one-dimensional', img.shape)
    img = np.uint8(np.clip(img, 0, 255))
    image_data = BytesIO()
    PIL.Image.fromarray(img).save(image_data, fmt)
    if filename is None:
        height, width = img.shape[:2]
        if zoom is not None:
            width *= zoom
            height *= zoom
        IPython.display.display(IPython.display.Image(data=image_data.getvalue(),
                                                      width=width,
                                                      height=height,
                                                      retina=retina))
    else:
        with open(filename, 'wb') as f:
            image_data.seek(0)
            shutil.copyfileobj(image_data, f)
