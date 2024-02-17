from OpenGL import GL


# static methods to load and compile shaders
class OpenGLUtils(object):
    @staticmethod
    def initialise_shader(shader_code, shader_type):
        """
        Initialises a given shader
        :param shader_code: code used by shader
        :param shader_type: whether a Vertex or Fragment
        :return:
        """
        # specify OpenGL version
        shader_code = "#version 330\n " + shader_code

        # create empty shader and return reference
        shader_ref = GL.glCreateShader(shader_type)
        # store source code in shader
        GL.glShaderSource(shader_ref, shader_code)
        # compile source code
        GL.glCompileShader(shader_ref)

        # check compilation was successful
        compile_success = GL.glGetShaderiv(shader_ref, GL.GL_COMPILE_STATUS)

        if not compile_success:
            # retrieve error message
            error_message = GL.glGetShaderInfoLog(shader_ref)
            GL.glDeleteShader(shader_ref)
            # convert byte string to char string
            error_message = "\n" + error_message.decode("utf-8")
            # raise exception
            raise Exception(error_message)

        # compilation success
        return shader_ref

    @staticmethod
    def initialise_program(vertex_shader_code, fragment_shader_code):
        """
        Initialises an OpenGL program using the two shaders
        :param vertex_shader_code: vertex shader to use
        :param fragment_shader_code: fragment shader to use
        :return:
        """
        # compile shaders and store refs
        vertex_shader_ref = OpenGLUtils.initialise_shader(
            vertex_shader_code, GL.GL_VERTEX_SHADER)
        fragment_shader_ref = OpenGLUtils.initialise_shader(
            fragment_shader_code, GL.GL_FRAGMENT_SHADER)

        # create program
        program_ref = GL.glCreateProgram()

        # attach compiled shaders
        GL.glAttachShader(program_ref, vertex_shader_ref)
        GL.glAttachShader(program_ref, fragment_shader_ref)

        # link vertex shader to fragment shader
        GL.glLinkProgram(program_ref)

        # check linking success
        link_success = GL.glGetProgramiv(program_ref, GL.GL_LINK_STATUS)
        if not link_success:
            # retrieve error message
            error_message = GL.glGetProgramInfoLog(program_ref)
            # free memory
            GL.glDeleteProgram(program_ref)

            error_message = "\n" + error_message.decode("utf-8")
            # raise exception
            raise Exception(error_message)

        # linking successful
        return program_ref
