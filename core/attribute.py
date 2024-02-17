import numpy as np
from OpenGL.GL import *


class Attribute(object):
    def __init__(self, data_type, data):
        """
        Creates an Attribute object
        :param data_type: data type of attribute
        :param data: data supplied to attribute
        """
        # Type of data in data array
        # can be int, float, vec2, vec3 or vec4
        self.data_type = data_type

        # Data array to be stored in buffer
        self.data = data

        # Reference to available buffer
        self.buffer_ref = glGenBuffers(1)

        # Upload data to buffer
        self.upload_data()

    def upload_data(self):
        """
        Uploads given data to a GPU buffer
        """
        # Convert data to numpy float array
        data = np.array(self.data).astype(np.float32)
        # Select buffer for use
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_ref)
        # Store data in bound buffer
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

    def associate_variable(self, program_ref, variable_name):
        """
        Associates variable in program to buffer
        :param program_ref: GPU program to use
        :param variable_name: name of variable
        """
        # Get reference for program variable
        variable_ref = glGetAttribLocation(program_ref, variable_name)
        # Check that program references variable
        if variable_ref == -1:
            return

        # Select buffer for use
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_ref)
        # Specify how data will be read from GL_ARRAY_BUFFER
        if self.data_type == "int":
            glVertexAttribPointer(variable_ref, 1, GL_INT, False, 0, None)
        elif self.data_type == "float":
            glVertexAttribPointer(variable_ref, 1, GL_FLOAT, False, 0, None)
        elif self.data_type == "vec2":
            glVertexAttribPointer(variable_ref, 2, GL_FLOAT, False, 0, None)
        elif self.data_type == "vec3":
            glVertexAttribPointer(variable_ref, 3, GL_FLOAT, False, 0, None)
        elif self.data_type == "vec4":
            glVertexAttribPointer(variable_ref, 4, GL_FLOAT, False, 0, None)
        else:
            raise Exception(f"Error: Unknown attribute data type {self.data_type}")

        # Stream data from variable to buffer
        glEnableVertexAttribArray(variable_ref)
