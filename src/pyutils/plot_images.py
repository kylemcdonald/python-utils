import numpy as np

def plot_images(images, xy, blend=np.maximum, canvas_shape=(512,512), fill=0):    
    h,w = images.shape[1:3]
    if images.ndim == 4:
        canvas_shape = (canvas_shape[0], canvas_shape[1], images.shape[3])
    
    min_xy = np.amin(xy, 0)
    max_xy = np.amax(xy, 0)
    
    min_canvas = np.array((0, 0))
    max_canvas = np.array((canvas_shape[0] - h, canvas_shape[1] - w))
    
    xy_mapped = min_canvas + (xy - min_xy) * (max_canvas - min_canvas) / (max_xy - min_xy)
    xy_mapped = xy_mapped.astype(int)
    
    canvas = np.full(canvas_shape, fill)
    for image, pos in zip(images, xy_mapped):
        x_off, y_off = pos
        sub_canvas = canvas[y_off:y_off+h, x_off:x_off+w]
        sub_image = image[:h, :w]
        try:
            canvas[y_off:y_off+h, x_off:x_off+w] = blend(sub_canvas, sub_image)
        except ValueError:
            print(pos, h, w, min_canvas, max_canvas)
            raise

    return canvas