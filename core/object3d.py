from core.matrix import Matrix
import numpy


class Object3D(object):
    def __init__(self):
        """
        Creates an Object3D
        """
        self.transform = Matrix.make_identity()
        self.parent = None
        self.children = []

    def add(self, child):
        """
        Adds a child object to this object
        :param child: child object
        """
        self.children.append(child)
        child.parent = self

    def remove(self, child):
        """
        Removes a child object from this object
        :param child: child object
        """
        self.children.remove(child)
        child.parent = None

    def get_world_matrix(self):
        """
        Calculates transformation matrix of current object in world coordinates
        :return: world transformation matrix
        """
        if self.parent is None:
            return self.transform
        else:
            return self.parent.get_world_matrix() @ self.transform

    def get_descendant_list(self):
        """
        Flattens scene tree into a single list of descendants
        :return: List of descendants
        """
        # Master list of all descendant nodes
        descendants = []

        # Depth-first search of tree
        nodes_to_process = [self]
        # continue processing whilst nodes left
        while len(nodes_to_process) > 0:
            # remove first node
            node = nodes_to_process.pop(0)
            # add to descendant list
            descendants.append(node)
            # add children to be processed
            nodes_to_process = node.children + nodes_to_process

        return descendants

    def apply_matrix(self, matrix, local_coord=True):
        """
        Applies given transformation matrix, in global or local coords
        :param matrix: transformation matrix
        :param local_coord: whether local or global
        """
        if local_coord:
            self.transform = self.transform @ matrix
        else:
            self.transform = matrix @ self.transform

    def translate(self, x, y, z, local_coord=True):
        """
        Applies translation to object
        :param x: movement in x
        :param y: movement in y
        :param z: movement in z
        :param local_coord: whether local or global
        """
        m = Matrix.make_translation(x, y, z)
        self.apply_matrix(m, local_coord)

    def rotate_x(self, angle, local_coord=True):
        """
        Applies rotation along x-axis on object
        :param angle: angle in radians
        :param local_coord: whether local or global
        """
        m = Matrix.make_rotation_x(angle)
        self.apply_matrix(m, local_coord)

    def rotate_y(self, angle, local_coord=True):
        """
        Applies rotation along y-axis on object
        :param angle: angle in radians
        :param local_coord: whether local or global
        """
        m = Matrix.make_rotation_y(angle)
        self.apply_matrix(m, local_coord)

    def rotate_z(self, angle, local_coord=True):
        """
        Applies rotation along z-axis on object
        :param angle: angle in radians
        :param local_coord: whether local or global
        """
        m = Matrix.make_rotation_z(angle)
        self.apply_matrix(m, local_coord)

    def scale(self, s, local_coord=True):
        """
        Applies scale to object
        :param s: scale ratio
        :param local_coord: whether local or global
        """
        m = Matrix.make_scale(s)
        self.apply_matrix(m, local_coord)

    def get_position(self):
        """
        Gets position components of transform
        :return: position components
        """
        return [
            self.transform.item((0, 3)),
            self.transform.item((1, 3)),
            self.transform.item((2, 3))
        ]

    def get_world_position(self):
        """
        Gets the position of transform in world coords
        :return: World position
        """
        world_transform = self.get_world_matrix()
        return [
            world_transform.item((0, 3)),
            world_transform.item((1, 3)),
            world_transform.item((2, 3))
        ]

    def set_position(self, position):
        """
        Sets position components of a transformation matrix
        :param position: [x, y, z]
        """
        self.transform.itemset((0, 3), position[0])
        self.transform.itemset((1, 3), position[1])
        self.transform.itemset((2, 3), position[2])

    def look_at(self, target_position):
        """
        Rotate an object as if it is looking at a specific target coordinate
        :param target_position: coordinate of target
        """
        self.transform = Matrix.make_look_at(self.get_world_position(), target_position)

    def get_rotation_matrix(self):
        """
        Gets a 3x3 submatrix containing rotation data
        :return: 3x3 rotation data submatrix
        """
        return numpy.array([
            self.transform[0][0:3],
            self.transform[1][0:3],
            self.transform[2][0:3]
        ])

    def get_direction(self):
        """
        Returns current direction relative to the local negative z-axis
        :return: current direction matrix
        """
        forward = numpy.array([0, 0, -1])
        return list(self.get_rotation_matrix() @ forward)

    def set_direction(self, direction):
        """
        Sets the direction of the object3D
        :param direction: target direction
        """
        position = self.get_position()
        target_position = [
            position[0] + direction[0],
            position[1] + direction[1],
            position[2] + direction[2]
        ]
        self.look_at(target_position)
