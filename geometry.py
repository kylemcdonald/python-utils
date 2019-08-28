import numpy as np
import math

# pair of points on lines p1,p2 and p3,p4 closest to each other
def line_line_closest(p1,p2,p3,p4):
    p13 = p1 - p3
    p43 = p4 - p3
    p21 = p2 - p1

    d1343 = p13[0] * p43[0] + p13[1] * p43[1] + p13[2] * p43[2]
    d4321 = p43[0] * p21[0] + p43[1] * p21[1] + p43[2] * p21[2]
    d1321 = p13[0] * p21[0] + p13[1] * p21[1] + p13[2] * p21[2]
    d4343 = p43[0] * p43[0] + p43[1] * p43[1] + p43[2] * p43[2]
    d2121 = p21[0] * p21[0] + p21[1] * p21[1] + p21[2] * p21[2]

    denom = d2121 * d4343 - d4321 * d4321
    # currently not checking for parallel lines
#     if abs(denom) < 0.000001:
#         return None, None
    numer = d1343 * d4321 - d1321 * d4343

    mua = numer / denom
    mub = (d1343 + d4321 * (mua)) / d4343

    pa = p1 + mua * p21
    pb = p3 + mub * p43

    return pa, pb

# point on line p1,p2 closest to point p3 
def line_point_closest(p1, p2, p3):
    p1 = np.asarray(p1)
    p2 = np.asarray(p2)
    p3 = np.asarray(p3)
    u = ((p3 - p1)*(p2 - p1)).sum() / np.square(np.linalg.norm(p2 - p1))
    return p1 + u * (p2 - p1)

# point on ray p1->p2 closest to point p3 
def ray_point_closest(p1, p2, p3):
    p1 = np.asarray(p1)
    p2 = np.asarray(p2)
    p3 = np.asarray(p3)
    u = ((p3 - p1)*(p2 - p1)).sum() / np.square(np.linalg.norm(p2 - p1))
    u = max(u, 0)
    return p1 + u * (p2 - p1)

# numpy multiplication order is "reversed" from openFrameworks,
# or the matrices can be transposed: A*B = B^T*A

# from 0/0 to width/height
# to -1,+1 to +1/-1 (y axis is flipped)
def screen_to_world(screen, depth, viewport, extrinsics, camera_matrix):
    principal_point = camera_matrix[:2,2]
    screen -= principal_point - (viewport - 1) / 2
    camera = [
        2 * screen[0] / viewport[0] - 1,
        1 - 2 * screen[1] / viewport[1],
        depth
    ]
    return camera_to_world(camera, extrinsics, viewport, camera_matrix)

def to_homogenous(xyz):
    return np.asarray([xyz[0], xyz[1], xyz[2], 1])

def from_homogenous(xyzw):
    return xyzw[:3] / xyzw[3]

def camera_to_world(camera, extrinsics, viewport, camera_matrix):
    mvp_matrix = get_model_view_projection_matrix(extrinsics, viewport, camera_matrix)
    world = np.matmul(to_homogenous(camera), np.linalg.inv(mvp_matrix))
    return from_homogenous(world)

def get_model_view_projection_matrix(extrinsics, viewport, camera_matrix):
    return np.matmul(get_model_view_matrix(extrinsics), get_projection_matrix(viewport, camera_matrix))
    
def get_model_view_matrix(extrinsics):
    return np.linalg.inv(extrinsics.T)

def perspective(fovy, aspect, z_near, z_far):
    tan_half_fovy = math.tan(fovy / 2)
    result = np.zeros((4,4))
    result[0,0] = 1 / (aspect * tan_half_fovy)
    result[1,1] = 1 / tan_half_fovy
    result[2,3] = -1
    result[2,2] = -(z_far + z_near) / (z_far - z_near)
    result[3,2] = -(2 * z_far * z_near) / (z_far - z_near)
    return result

def get_projection_matrix(viewport, camera_matrix, z_near=1, z_far=1000):
    aspect = viewport[0] / viewport[1]
    fovy = 2 * math.atan(viewport[1] / (2 * camera_matrix[1,1]))
    return perspective(fovy, aspect, z_near, z_far)