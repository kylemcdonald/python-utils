from skimage.draw import circle, circle_perimeter
from skimage.draw import polygon, polygon_perimeter
import cv2

def draw_line(canvas, pt1, pt2, r=1, stroke=None):
    cv2.line(canvas, pt1, pt2, stroke, thickness=r, lineType=cv2.LINE_AA)

def draw_circle(canvas, xy, r=1, stroke=None, fill=None):
    x,y = xy
    if fill:
        rr,cc = circle(y, x, r, shape=canvas.shape)
        canvas[rr,cc] = fill
    if stroke:
        rr,cc = circle_perimeter(y, x, r, shape=canvas.shape)
        canvas[rr,cc] = stroke

def draw_rectangle(canvas, rect, fill=None, stroke=None):
    t,b,l,r = rect
    t = int(max(t,0))
    b = int(min(b,canvas.shape[0]-1))
    l = int(max(l,0))
    r = int(min(r,canvas.shape[1]-1))
    if fill is not None:
        canvas[t:b,l:r] = fill
    if stroke is not None:
        b -= 1
        r -= 1
        try:
            canvas[t:b,l] = stroke
        except IndexError:
            pass
        try:
            canvas[t:b,r] = stroke
        except IndexError:
            pass
        try:
            canvas[t,l:r] = stroke
        except IndexError:
            pass
        try:
            canvas[b,l:r+1] = stroke
        except IndexError:
            pass
        
def draw_rectangle_dlib(canvas, det, fill=None, stroke=None):
    rect = (det.top(), det.bottom(), det.left(), det.right())
    draw_rectangle(canvas, rect, fill=fill, stroke=stroke)
    