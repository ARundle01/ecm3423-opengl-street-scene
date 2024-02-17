from material.material import Material


class CubeMapMaterial(Material):
    """
    A material which uses a cube-map for texturing
    """
    def __init__(self, cube_map):
        vs_code = """
        uniform mat4 projection_matrix;
        uniform mat4 view_matrix;
        uniform mat4 model_matrix;
        
        in vec3 vertex_position;
        out vec3 tex_coords;
        
        void main() {
            vec4 pos = projection_matrix * view_matrix * model_matrix * vec4(vertex_position, 1);
            gl_Position = pos;
            gl_Position.z = gl_Position.w*0.9999;
            tex_coords = -vertex_position;
        }
        """

        fs_code = """
        uniform samplerCube cube_map;
        
        in vec3 tex_coords;
        out vec4 fragColor;
        
        void main() {
            fragColor = texture(cube_map, tex_coords);
        }
        """

        super().__init__(vs_code, fs_code)

        # Add the cube-map as a uniform
        self.add_uniform("samplerCube", "cube_map", [cube_map.texture_ref, 1])
        self.locate_uniforms()
