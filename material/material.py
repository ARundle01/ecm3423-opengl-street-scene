from core.openGLUtils import OpenGLUtils
from core.uniform import Uniform
from OpenGL.GL import *


class Material(object):
    """
    A class holding all details of the material of a mesh and handles shaders
    """
    def __init__(self, vs_code, fs_code):
        self.program_ref = OpenGLUtils.initialise_program(vs_code, fs_code)

        # Store Uniform objects
        self.uniforms = {}
        # Standard Uniform objects
        self.uniforms["model_matrix"] = Uniform("mat4", None)
        self.uniforms["view_matrix"] = Uniform("mat4", None)
        self.uniforms["projection_matrix"] = Uniform("mat4", None)

        # Store OpenGL render settings
        self.settings = {}
        self.settings["draw_style"] = GL_TRIANGLES

    def add_uniform(self, data_type, variable_name, data):
        """
        Adds new uniform to program
        :param data_type: data type of uniform
        :param variable_name: name of uniform
        :param data: data to be put into uniform
        """
        self.uniforms[variable_name] = Uniform(data_type, data)

    def locate_uniforms(self):
        """
        Initialises all Uniform variable references
        """
        for variable_name, uniform_object in self.uniforms.items():
            uniform_object.locate_variable(self.program_ref, variable_name)

    def update_render_settings(self):
        """
        Configure OpenGL render settings; extended by subclasses
        """
        pass

    def set_properties(self, properties={}):
        """
        Sets properties (Uniforms and Render Settings)
        :param properties: Uniforms and Render Settings to be set
        """
        for name, data in properties.items():
            # Update uniforms
            if name in self.uniforms.keys():
                self.uniforms[name].data = data
            # Update render settings
            elif name in self.settings.keys():
                self.settings[name] = data
            # Unknown property
            else:
                raise Exception(f"Material has no property: {name}")
