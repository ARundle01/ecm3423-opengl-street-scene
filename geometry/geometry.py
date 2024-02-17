import numpy as np
from core.attribute import Attribute


class Geometry(object):
    def __init__(self):
        """
        Creates the superclass of all geometry objects, storing attributes and vertice count
        """
        # Create dictionary to store attribute objects
        self.attributes = {}
        # Store number of vertices
        self.vertex_count = None

    def count_vertices(self):
        """
        Counts number of vertices to render
        """
        # Number of vertices = length of Attribute Object's array of data
        attrib = list(self.attributes.values())[0]
        self.vertex_count = len(attrib.data)

    def add_attribute(self, data_type, variable_name, data):
        """
        Adds an attribute to this geometry
        :param data_type: data type of this attribute
        :param variable_name: variable name to be referenced
        :param data: the data to be stored in the attribute
        """
        self.attributes[variable_name] = Attribute(data_type, data)

    def apply_matrix(self, matrix, variable_name="vertex_position"):
        """
        Applies a given matrix to a given attribute of the geometry
        :param matrix: Matrix to apply
        :param variable_name: attribute to be applied to
        """
        # Update vertex position data
        old_position_data = self.attributes[variable_name].data
        new_position_data = []

        for old_position in old_position_data:
            # Avoid changing list refs
            new_position = old_position.copy()
            # Add homogeneous coord
            new_position.append(1)
            # Multiply by matrix
            new_position = matrix @ new_position
            # Remove homogeneous coord
            new_position = list(new_position[0:3])
            # Add to new data list
            new_position_data.append(new_position)
        self.attributes[variable_name].data = new_position_data

        # Extract rotation submatrix
        rotation_matrix = np.array([
            matrix[0][0:3],
            matrix[1][0:3],
            matrix[2][0:3]
        ])

        # Update vertex normal data
        old_vertex_normal_data = self.attributes["vertex_normal"].data
        new_vertex_normal_data = []

        for old_normal in old_vertex_normal_data:
            new_normal = old_normal.copy()
            new_normal = rotation_matrix @ new_normal
            new_vertex_normal_data.append(new_normal)
        self.attributes["vertex_normal"].data = new_vertex_normal_data

        old_face_normal_data = self.attributes["face_normal"].data
        new_face_normal_data = []
        for old_normal in old_face_normal_data:
            new_normal = old_normal.copy()
            new_normal = rotation_matrix @ new_normal
            new_face_normal_data.append(new_normal)
        self.attributes["face_normal"].data = new_face_normal_data

        # Upload new data
        self.attributes[variable_name].upload_data()

    def merge(self, other_geometry):
        """
        Merges current geometry with another geometry object
        :param other_geometry: other geometry to merge with
        """
        for variable_name, attribute_object in self.attributes.items():
            attribute_object.data += other_geometry.attributes[variable_name].data
            # Upload new data
            attribute_object.upload_data()

        # Update number of vertices
        self.count_vertices()
