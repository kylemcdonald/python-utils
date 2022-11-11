import cv2

def draw_line(canvas, pt1, pt2, r=1, stroke=None):
    pt1 = tuple(map(int, pt1))
    pt2 = tuple(map(int, pt2))
    cv2.line(canvas, pt1, pt2, stroke, thickness=r, lineType=cv2.LINE_AA)

def draw_text(canvas, text, xy, color=0, scale=1, thickness=1, highlight=None,
        font_face=cv2.FONT_HERSHEY_SIMPLEX, antialias=False):
    l,t = tuple(map(int, xy))
    (tw,th), baseline = cv2.getTextSize(text, font_face, scale, thickness)
    t += th + baseline - 1
    if highlight is not None:
        canvas[t-th-baseline-1:t,l:l+tw] = highlight
    cv2.putText(canvas, text, (l,t-baseline), font_face, scale, color, thickness, cv2.LINE_AA if antialias else 0)

# for some reason a fill of 0 doesn't work, but 0.1 does work
def draw_circle(canvas, xy, r=1, stroke=None, fill=None, thickness=1, antialias=False):
    x,y = tuple(map(int, xy))
    line_type = cv2.LINE_AA if antialias else cv2.LINE_8
    if fill is not None:
        cv2.circle(canvas, (x,y), r, fill, -1, line_type)
    if stroke is not None:
        cv2.circle(canvas, (x,y), r, stroke, thickness, line_type)

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

def draw_rectangle_thin(canvas, tblr, fill=None, stroke=None):
    t,b,l,r = tblr
    ye = canvas.shape[0] - 1
    xe = canvas.shape[1] - 1
    t = int(min(max(t,0),ye))
    b = int(min(max(b,0),ye))
    l = int(min(max(l,0),xe))
    r = int(min(max(r,0),xe))
    if fill is not None:
        canvas[t:b,l:r] = fill
    if stroke is not None:
        b = int(max(b-1,0))
        r = int(max(r-1,0))
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
            r = int(min(r+1,xe))
            canvas[b,l:r] = stroke
        except IndexError:
            pass
        
def draw_rectangle(canvas, tblr, fill=None, stroke=None, thickness=1):
    draw_rectangle_thin(canvas, tblr, fill, stroke)
    for i in range(1, thickness):
        t,b,l,r = tblr
        draw_rectangle_thin(canvas, (t-i,b+i,l-i,r+i), fill, stroke)
        draw_rectangle_thin(canvas, (t+i,b-i,l+i,r-i), fill, stroke)
        
def draw_rectangle_dlib(canvas, det, fill=None, stroke=None):
    rect = (det.top(), det.bottom(), det.left(), det.right())
    draw_rectangle(canvas, rect, fill=fill, stroke=stroke)

