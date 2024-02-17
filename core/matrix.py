import numpy as np
from math import sin, cos, tan, pi
from numpy import subtract, divide, cross
from numpy.linalg import norm


class Matrix(object):
    """
    Specifies methods for generating and modifying matrices
    """
    @staticmethod
    def make_identity():
        """
        Returns the identity matrix
        :return: Identity matrix
        """
        return np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]]).astype(float)

    @staticmethod
    def make_translation(x, y, z):
        """
        Returns a translation matrix using x, y, z
        :param x: movement in x-axis
        :param y: movement in y-axis
        :param z: movement in z-axis
        :return: translation matrix
        """
        return np.array([[1, 0, 0, x],
                         [0, 1, 0, y],
                         [0, 0, 1, z],
                         [0, 0, 0, 1]]).astype(float)

    @staticmethod
    def make_rotation_x(angle):
        """
        Returns a rotation matrix around x-axis
        :param angle: angle in radians
        :return: Rotation matrix
        """
        c = cos(angle)
        s = sin(angle)
        return np.array([[1, 0, 0, 0],
                         [0, c, -s, 0],
                         [0, s, c, 0],
                         [0, 0, 0, 1]]).astype(float)

    @staticmethod
    def make_rotation_y(angle):
        """
        Returns rotation matrix around y-axis
        :param angle: angle in radians
        :return: Rotation matrix
        """
        c = cos(angle)
        s = sin(angle)
        return np.array([[c, 0, s, 0],
                         [0, 1, 0, 0],
                         [-s, 0, c, 0],
                         [0, 0, 0, 1]]).astype(float)

    @staticmethod
    def make_rotation_z(angle):
        """
        Returns rotation matrix around z-axis
        :param angle: angle in radians
        :return: Rotation matrix
        """
        c = cos(angle)
        s = sin(angle)
        return np.array([[c, -s, 0, 0],
                         [s, c, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]]).astype(float)

    @staticmethod
    def make_scale(s):
        """
        Returns a scale matrix
        :param s: scale coefficient
        :return: scale matrix
        """
        return np.array([[s, 0, 0, 0],
                         [0, s, 0, 0],
                         [0, 0, s, 0],
                         [0, 0, 0, 1]]).astype(float)

    @staticmethod
    def make_perspective(angle_of_view=60, aspect_ratio=1, near=0.1, far=100):
        """
        Returns a projection matrix for the frustum
        :param angle_of_view: angle in degrees
        :param aspect_ratio: aspect ratio
        :param near: distance to near plane
        :param far: distance to far plane
        :return: Projection matrix
        """
        a = angle_of_view * pi/180
        d = 1.0 / tan(a/2)
        r = aspect_ratio
        b = (far + near)/(near - far)
        c = 2 * far * near / (near - far)
        return np.array([[d/r, 0, 0, 0],
                         [0, d, 0, 0],
                         [0, 0, b, c],
                         [0, 0, -1, 0]]).astype(float)

    @staticmethod
    def make_look_at(position, target):
        """
        Creates a look at matrix, forcing an object to look at a given target coord
        :param position: position of object
        :param target: position of target
        :return: Look-at matrix
        """
        world_up = [0, 1, 0]
        forward = subtract(target, position)
        right = cross(forward, world_up)

        # If the forward and world_up vectors are parallel,
        # right vector is zero, so perturb world_up vector
        if norm(right) < 0.001:
            offset = np.array([0.001, 0, 0])
            right = cross(forward, world_up + offset)

        up = cross(right, forward)

        # All vectors should have length 1
        forward = divide(forward, norm(forward))
        right = divide(right, norm(right))
        up = divide(up, norm(up))

        return np.array([
            [right[0], up[0], -forward[0], position[0]],
            [right[1], up[1], -forward[1], position[1]],
            [right[2], up[2], -forward[2], position[2]],
            [0, 0, 0, 1]
        ])
