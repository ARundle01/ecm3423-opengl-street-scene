from material.material import Material
from OpenGL.GL import *


class TextureMaterial(Material):
    """
    A shader with no shading, but applies a texture
    """
    def __init__(self, texture, properties={}):
        vs_code = """
        uniform mat4 projection_matrix;
        uniform mat4 view_matrix;
        uniform mat4 model_matrix;
        in vec3 vertex_position;
        in vec2 vertex_uv;
        out vec2 UV;
        
        void main() {
            gl_Position = projection_matrix * view_matrix * model_matrix * vec4(vertex_position, 1);
            UV = vertex_uv;
        }
        """

        fs_code = """
        uniform vec3 base_colour;
        uniform sampler2D texture;
        in vec2 UV;
        out vec4 fragColor;
        
        void main() {
            vec4 colour = vec4(base_colour, 1);
            fragColor = colour * texture2D(texture, UV);
        }
        """

        super().__init__(vs_code, fs_code)

        self.add_uniform("vec3", "base_colour", [1, 1, 1])
        # Supply texture as a uniform
        self.add_uniform("sampler2D", "texture", [texture.texture_ref, 1])
        self.locate_uniforms()

        # Set up render settings
        self.settings["double_side"] = True
        self.settings["wireframe"] = False
        self.settings["line_width"] = 1
        self.set_properties(properties)

    def update_render_settings(self):
        """
        Updates render settings if supplied in properties
        """
        if self.settings["double_side"]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)

        if self.settings["wireframe"]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINES)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glLineWidth(self.settings["line_width"])
