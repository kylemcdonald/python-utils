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

# pivot can be percentage or pixels
def rotate_image(img, angle, pivot=(0.5, 0.5), scale=1.0, borderValue=(128,128,128)):
    h,w = img.shape[:2]
    if len(img.shape) == 2 and hasattr(borderValue, '__len__'):
        borderValue = borderValue[0]
    if pivot[0] < 1 and pivot[1] < 1:
        pivot = (int(w * pivot[0]), int(h * pivot[1]))
    matrix = cv2.getRotationMatrix2D(pivot, angle, scale)
    return cv2.warpAffine(img, matrix, (w, h),
                          flags=cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_CONSTANT,
                          borderValue=borderValue)