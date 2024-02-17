from core.object3d import Object3D
from OpenGL.GL import *


class Mesh(Object3D):
    """
    Sets associations between attributes and shader variables
    """
    def __init__(self, geometry, material):
        """
        Creates a mesh
        :param geometry: geometry of mesh
        :param material: material to be used by mesh
        """
        super().__init__()

        # Geometry and material to be used by mesh
        self.geometry = geometry
        self.material = material

        # Visibility boolean
        self.visible = True

        # Set associations between attributes in geometry and shader variables in material
        self.vao_ref = glGenVertexArrays(1)
        glBindVertexArray(self.vao_ref)
        for variable_name, attribute_object in geometry.attributes.items():
            attribute_object.associate_variable(material.program_ref, variable_name)
        # Unbind VAO
        glBindVertexArray(0)
