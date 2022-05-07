import numpy as np
import math

# angle between two vectors
def vector_vector_angle(v1, v2):
    a1 = np.arctan2(v1[1], v1[0])
    a2 = np.arctan2(v2[1], v2[0])
    sign = 1 if a1 > a2 else -1
    angle = a1 - a2
    K = -sign * np.pi * 2
    if np.abs(K + angle) < np.abs(angle):
        angle += K
    return angle

# pair of points on lines p1,p2 and p3,p4 closest to each other
def line_line_closest(p1,p2,p3,p4,check=False):
    p1 = np.asarray(p1)
    p2 = np.asarray(p2)
    p3 = np.asarray(p3)
    p4 = np.asarray(p4)

    p13 = p1 - p3
    p43 = p4 - p3
    p21 = p2 - p1

    d1343 = np.dot(p13, p43)
    d4321 = np.dot(p43, p21)
    d1321 = np.dot(p13, p21)
    d4343 = np.dot(p43, p43)
    d2121 = np.dot(p21, p21)

    denom = d2121 * d4343 - d4321 * d4321
    if check and abs(denom) == 0:
        return None
    numer = d1343 * d4321 - d1321 * d4343

    mua = numer / denom
    mub = (d1343 + d4321 * (mua)) / d4343

    if check:
        if mua < 0 or mua > 1 or mub < 0 or mub > 1:
            return None

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
# note that depth is not in world units, but normalized by z_near/z_far
# designed for multiple points
def screen_to_world(screen, depth, viewport, extrinsics, camera_matrix):
    principal_point = camera_matrix[:2,2]
    screen -= principal_point - (viewport - 1) / 2
    n = len(screen)
    camera = np.array([
        2 * screen[:,0] / viewport[0] - 1,
        1 - 2 * screen[:,1] / viewport[1],
        [depth] * n
    ])
    camera = camera.T
    return camera_to_world(camera, extrinsics, viewport, camera_matrix)

def to_homogenous(points):
    ones = np.ones((len(points), 1), points.dtype)
    return np.hstack((points, ones))

def from_homogenous(xyzw):
    return xyzw[:,:3] / xyzw[:,3].reshape(-1,1)

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
    
def vec_to_extrinsics(rvec,tvec):
    R, jacobian = cv2.Rodrigues(np.mat(rvec))
    arr = np.array([[R[0,0],R[0,1],R[0,2],tvec[0]],
                    [R[1,0],R[1,1],R[1,2],tvec[1]],
                    [R[2,0],R[2,1],R[2,2],tvec[2]],
                    [0,0,0,1]])
    mat = np.mat(arr)
    extrinsics = np.transpose(np.linalg.inv(mat))
    return extrinsics
