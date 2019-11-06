import cv2

def draw_line(canvas, pt1, pt2, r=1, stroke=None):
    pt1 = tuple(map(int, pt1))
    pt2 = tuple(map(int, pt2))
    cv2.line(canvas, pt1, pt2, stroke, thickness=r, lineType=cv2.LINE_AA)

def draw_text(canvas, text, xy, color=0, scale=1, thickness=1, highlight=None,
        font_face=cv2.FONT_HERSHEY_SIMPLEX, antialias=False):
    l,t = xy
    (tw,th), baseline = cv2.getTextSize(text, font_face, scale, thickness)
    t += th + baseline - 1
    if highlight is not None:
        canvas[t-th-baseline-1:t,l:l+tw] = highlight
    cv2.putText(canvas, text, (l,t-baseline), font_face, scale, color, thickness, cv2.LINE_AA if antialias else 0)

def draw_circle(canvas, xy, r=1, stroke=None, fill=None):
    from skimage.draw import circle, circle_perimeter
    x,y = tuple(map(int, xy))
    if fill:
        rr,cc = circle(y, x, r, shape=canvas.shape)
        canvas[rr,cc] = fill
    if stroke:
        rr,cc = circle_perimeter(y, x, r, shape=canvas.shape)
        canvas[rr,cc] = stroke

# @njit
# def draw_circle(canvas, xy, r, fill):
#     x,y = xy
#     r2 = r * r
#     for i in range(canvas.shape[0]):
#         cy = i - y
#         cy2 = cy * cy
#         for j in range(canvas.shape[1]):
#             cx = j - x
#             ls = cx * cx + cy2
#             if ls < r2:
#                 canvas[i,j] = fill     

def draw_rectangle(canvas, tblr, fill=None, stroke=None):
    t,b,l,r = tblr
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

