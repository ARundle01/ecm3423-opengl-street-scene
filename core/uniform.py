from OpenGL.GL import *


class Uniform(object):
    """
    Defines Uniform object to be used by and passed to shaders
    """
    def __init__(self, data_type, data):
        """
        Creates a Uniform object
        :param data_type: data type of uniform
        :param data: data to be supplied to shader as a uniform
        """
        self.data_type = data_type
        self.data = data

        # Reference to variable location in program
        self.variable_ref = None

    def locate_variable(self, program_ref, variable_name):
        """
        Locates variable in program
        :param program_ref: reference in memory to OpenGL program
        :param variable_name: name of variable
        :return:
        """
        if self.data_type == "Light":
            self.variable_ref = {}
            self.variable_ref["light_type"] = glGetUniformLocation(program_ref, variable_name + ".light_type")
            self.variable_ref["colour"] = glGetUniformLocation(program_ref, variable_name + ".colour")
            self.variable_ref["direction"] = glGetUniformLocation(program_ref, variable_name + ".direction")
            self.variable_ref["position"] = glGetUniformLocation(program_ref, variable_name + ".position")
            self.variable_ref["attenuation"] = glGetUniformLocation(program_ref, variable_name + ".attenuation")
        else:
            self.variable_ref = glGetUniformLocation(program_ref, variable_name)

    def add_uniform(self, data_type, variable_name, data):
        """
        Adds a uniform to the uniforms list
        :param data_type: data type of uniform
        :param variable_name: name of uniform in shaders
        :param data: data to send to uniform
        """
        self.uniforms[variable_name] = Uniform(data_type, data)

    def upload_data(self):
        """
        Uploads uniform data to the shaders
        """
        # check if variable exists
        if self.variable_ref == -1:
            return

        if self.data_type == "int":
            glUniform1i(self.variable_ref, self.data)
        elif self.data_type == "bool":
            glUniform1i(self.variable_ref, self.data)
        elif self.data_type == "float":
            glUniform1f(self.variable_ref, self.data)
        elif self.data_type == "vec2":
            glUniform2f(self.variable_ref, self.data[0], self.data[1])
        elif self.data_type == "vec3":
            glUniform3f(self.variable_ref, self.data[0], self.data[1], self.data[2])
        elif self.data_type == "vec4":
            glUniform4f(self.variable_ref, self.data[0], self.data[1], self.data[2], self.data[3])
        elif self.data_type == "mat4":
            glUniformMatrix4fv(self.variable_ref, 1, GL_TRUE, self.data)
        elif self.data_type == "sampler2D":
            texture_object_ref, texture_unit_ref = self.data
            # Activate texture unit
            glActiveTexture(GL_TEXTURE0 + texture_unit_ref)
            # Associate object to active unit
            glBindTexture(GL_TEXTURE_2D, texture_object_ref)
            # Upload texture unit to uniform variable in shader
            glUniform1i(self.variable_ref, texture_unit_ref)
        elif self.data_type == "samplerCube":
            texture_object_ref, texture_unit_ref = self.data
            glActiveTexture(GL_TEXTURE0 + texture_unit_ref)
            glBindTexture(GL_TEXTURE_CUBE_MAP, texture_object_ref)
            glUniform1i(self.variable_ref, texture_unit_ref)
        elif self.data_type == "Light":
            glUniform1i(self.variable_ref["light_type"], self.data.light_type)
            glUniform3f(self.variable_ref["colour"], self.data.colour[0], self.data.colour[1], self.data.colour[2])

            direction = self.data.get_direction()
            glUniform3f(self.variable_ref["direction"], direction[0], direction[1], direction[2])

            position = self.data.get_position()
            glUniform3f(self.variable_ref["position"], position[0], position[1], position[2])

            glUniform3f(self.variable_ref["attenuation"],
                        self.data.attenuation[0],
                        self.data.attenuation[1],
                        self.data.attenuation[2])
        else:
            raise Exception(f"Unknown Uniform data type: {self.data_type}")
