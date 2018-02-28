import numpy as np

def map_range(x, in_min, in_max, out_min, out_max):
    return out_min + (out_max - out_min) * (x - in_min) / (in_max - in_min)

def plot_images(images, xy, blend=np.maximum, canvas_shape=(512,512), fill=0):    
    h,w = images.shape[1:3]
    if images.ndim == 4:
        canvas_shape = (canvas_shape[0], canvas_shape[1], images.shape[3])
    
    min_xy = np.amin(xy, 0)
    max_xy = np.amax(xy, 0)
    
    min_canvas = np.array((0, 0))
    max_canvas = np.array((canvas_shape[0] - h, canvas_shape[1] - w))
    
    canvas = np.full(canvas_shape, fill)
    for image, pos in zip(images, xy):
        x_off, y_off = map_range(pos, min_xy, max_xy, min_canvas, max_canvas).astype(int)
        sub_canvas = canvas[y_off:y_off+h, x_off:x_off+w]
        sub_image = image[:h, :w]
        canvas[y_off:y_off+h, x_off:x_off+w] = blend(sub_canvas, sub_image)

    return canvas