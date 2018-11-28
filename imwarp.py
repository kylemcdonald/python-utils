import cv2
import numpy as np

def translate_image(img, xy, borderValue=(128,128,128)):
    h,w = img.shape[:2]
    if len(img.shape) == 2 and hasattr(borderValue, '__len__'):
        borderValue = borderValue[0]
    x,y = xy
    matrix = np.float32([[1,0,x],[0,1,y]])
    return cv2.warpAffine(img, matrix, (w,h),
                          flags=cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_CONSTANT,
                          borderValue=borderValue)

# pivot is y,x pixels, pivot_percent in ratio to height and width
def rotate_image(img, angle, pivot_percent=(0.5, 0.5), pivot=None, scale=1.0, borderValue=(128,128,128)):
    h,w = img.shape[:2]
    if len(img.shape) == 2 and hasattr(borderValue, '__len__'):
        borderValue = borderValue[0]
    if pivot is None:
        pivot = (int(h * pivot_percent[0]), int(w * pivot_percent[1]))
    matrix = cv2.getRotationMatrix2D((pivot[1], pivot[0]), angle, scale) # uses x, y pivot
    return cv2.warpAffine(img, matrix, (w, h),
                          flags=cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_CONSTANT,
                          borderValue=borderValue)