from material.material import Material


class EnvironmentMapMaterial(Material):
    """
    A material which applies reflections based on a given cube-map
    """
    def __init__(self, enviro_map, properties={}):
        vs_code = """
        in vec3 vertex_position;
        in vec3 vertex_normal;
        
        out vec3 position;
        out vec3 normal;
        
        uniform mat4 projection_matrix;
        uniform mat4 view_matrix;
        uniform mat4 model_matrix;
        
        void main() {
            gl_Position = projection_matrix * view_matrix * model_matrix * vec4(vertex_position, 1.0f);
            
            mat4 VM = view_matrix * model_matrix;
            mat3 VMi = mat3(inverse(VM));
            mat3 VMiT = transpose(VMi);
            
            position = vec3(view_matrix * model_matrix * vec4(vertex_position, 1.0f));
            normal = normalize(VMiT * vertex_normal);
        }
        """

        fs_code = """
        in vec3 normal;
        in vec3 position;
        out vec4 fragColor;
        
        uniform samplerCube sampler_cube;
        uniform mat4 projection_matrix;
        uniform mat4 view_matrix;
        uniform mat4 model_matrix;
        uniform float reflectivity;
        uniform vec3 base_colour;
        uniform bool is_full_reflect;
                
        void main() {
            vec3 norm_normal = normalize(normal);
            vec3 reflected = reflect(normalize(-position), norm_normal);
            mat3 VT = mat3(transpose(view_matrix));
            vec3 reflected_vector = normalize(VT * reflected);
            vec4 reflected_colour = texture(sampler_cube, reflected_vector);
            
            fragColor = mix(vec4(base_colour, 1.0), reflected_colour, reflectivity);
        }
        """

        super().__init__(vs_code, fs_code)

        # Add cube-map as uniform, for reflection
        self.add_uniform("samplerCube", "sampler_cube", [enviro_map.texture_ref, 1])

        if "base_colour" in properties.keys():
            self.add_uniform("vec3", "base_colour", properties["base_colour"])
        else:
            self.add_uniform("vec3", "base_colour", [1, 1, 1])

        if "reflectivity" in properties.keys():
            self.add_uniform("float", "reflectivity", properties["reflectivity"])
        else:
            self.add_uniform("float", "reflectivity", 0.6)

        self.locate_uniforms()
