from skimage.draw import circle, circle_perimeter
from skimage.draw import polygon, polygon_perimeter

def draw_circle(canvas, xy, r=1, stroke=None, fill=None):
    x,y = xy
    if fill:
        rr,cc = circle(y, x, r, shape=canvas.shape)
        canvas[rr,cc] = fill
    if stroke:
        rr,cc = circle_perimeter(y, x, r, shape=canvas.shape)
        canvas[rr,cc] = stroke

def draw_rectangle_original(canvas, det, fill=None, stroke=None):
    n,e,s,w = (det.top(), det.right(), det.bottom(), det.left())
    x,y = (n,n,s,s), (w,e,e,w)
    if fill:
        rr,cc = polygon(y, x, shape=canvas.shape)
        canvas[rr,cc] = fill
    if stroke:
        rr,cc = polygon_perimeter(y, x, shape=canvas.shape)
        canvas[rr,cc] = stroke
        
def draw_rectangle(canvas, rect, fill=None, stroke=None):
    t,b,l,r = rect
    t = max(t,0)
    b = min(b,canvas.shape[0]-1)
    l = max(l,0)
    r = min(r,canvas.shape[1]-1)
    if fill is not None:
        canvas[t:b,l:r] = fill
    if stroke is not None:
        b -= 1
        r -= 1
        canvas[t:b,l] = stroke
        canvas[t:b,r] = stroke
        canvas[t,l:r] = stroke
        canvas[b,l:r+1] = stroke