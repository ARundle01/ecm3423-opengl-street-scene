from material.material import Material


class LambertMaterial(Material):
    """
    A material which uses Lambert's cosine law for shading
    """
    def __init__(self, texture=None, properties={}):
        vs_code = """
        uniform mat4 projection_matrix;
        uniform mat4 view_matrix;
        uniform mat4 model_matrix;
        
        in vec3 vertex_position;
        in vec2 vertex_uv;
        in vec3 vertex_normal;
        
        out vec3 position;
        out vec2 UV;
        out vec3 normal;
        
        void main() {
            gl_Position = projection_matrix * view_matrix * model_matrix * vec4(vertex_position, 1);
            position = vec3(model_matrix * vec4(vertex_position, 1));
            UV = vertex_uv;
            
            normal = normalize(mat3(model_matrix) * vertex_normal);
        }
        """

        fs_code = """
        struct Light {
            int light_type;
            vec3 colour;
            vec3 direction;
            vec3 position;
            vec3 attenuation;
        };

        uniform Light light0;
        uniform Light light1;
        uniform Light light2;
        uniform Light light3;

        vec3 lightCalc(Light light, vec3 point_position, vec3 point_normal) {
            float ambient = 0;
            float diffuse = 0;
            float specular = 0;
            float attenuation = 1;
            vec3 light_direction = vec3(0, 0, 0);

            if (light.light_type == 1)
            {
                ambient = 1;
            }
            else if (light.light_type == 2)
            {
                light_direction = normalize(light.direction);
            }
            else if (light.light_type == 3)
            {
                light_direction = normalize(point_position - light.position);
                float distance = length(light.position - point_position);

                attenuation = 1.0 / (light.attenuation[0] +
                                    light.attenuation[1] * distance +
                                    light.attenuation[2] * distance * distance);
            }

            if (light.light_type > 1)
            {
                point_normal = normalize(point_normal);
                diffuse = max(dot(point_normal, -light_direction), 0.0);
                diffuse *= attenuation;
            }

            return light.colour * (ambient + diffuse + specular);
        }
        
        uniform vec3 base_colour;
        uniform bool use_texture;
        uniform sampler2D texture;
        
        in vec3 position;
        in vec2 UV;
        in vec3 normal;
        
        out vec4 fragColor;
        
        void main() {
            vec4 colour = vec4(base_colour, 1.0);
            
            if (use_texture)
            {
                colour *= texture2D(texture, UV);
            }
            
            vec3 total = vec3(0, 0, 0);
            total += lightCalc(light0, position, normal);
            total += lightCalc(light1, position, normal);
            total += lightCalc(light2, position, normal);
            total += lightCalc(light3, position, normal);
            
            colour *= vec4(total, 1);
            fragColor = colour;
        }
        """
        super().__init__(vs_code, fs_code)
        if "base_colour" in properties.keys():
            self.add_uniform("vec3", "base_colour", properties["base_colour"])
        else:
            self.add_uniform("vec3", "base_colour", [1, 1, 1])
        # Add uniforms for the 4 lights
        self.add_uniform("Light", "light0", None)
        self.add_uniform("Light", "light1", None)
        self.add_uniform("Light", "light2", None)
        self.add_uniform("Light", "light3", None)
        self.add_uniform("bool", "use_texture", 0)

        # Apply texture if supplied
        if texture is None:
            self.add_uniform("bool", "use_texture", False)
        else:
            self.add_uniform("bool", "use_texture", True)
            self.add_uniform("sampler2D", "texture", [texture.texture_ref, 1])

        self.locate_uniforms()
