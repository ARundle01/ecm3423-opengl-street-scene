import os
from geometry.geometry import Geometry


class OBJGeometry(Geometry):
    """
    Creates geometry based on an imported OBJ file, found in ../Graphics CA/models
    """
    def __init__(self, file_name="", has_normals=True):
        """
        Creates geometry from model's file name
        :param file_name: file name of model to load
        :param has_normals: whether model has pre-generated normals
        """
        super().__init__()

        # Navigate to ../models directory, assumed where all models are
        os.chdir(os.getcwd() + "/models")

        # Open OBJ, get contents as string, close OBJ
        print(f"Loading OBJ model from: ../Graphics CA/models/{file_name}")
        obj_file = open(file_name)
        obj_content_string = obj_file.read()
        obj_file.close()

        # Navigate back to root for next model to correctly import
        os.chdir(os.path.dirname(os.getcwd()))

        # Initialise position, texture uv and normal lists
        position_list = []
        uv_list = []
        normal_list = []

        # Convert string to array
        obj_contents = obj_content_string.splitlines()

        # Initialise lists to go to buffers
        vertex_position_data = []
        vertex_uv_data = []
        vertex_normal_data = []

        # Handle each line
        for line in obj_contents:
            # Remove whitespace
            if len(line.strip()) == 0:
                continue

            # Split line into string tokens
            values = line.split()

            # Add vertex data to position_list
            if values[0] == 'v':
                position_list.append([float(values[1]), float(values[2]), float(values[3])])
            # Add vertex uv data to list
            elif values[0] == 'vt':
                uv_list.append([float(values[1]), float(values[2])])
            # Add vertex normal data to list
            elif values[0] == 'vn':
                normal_list.append([float(values[1]), float(values[2]), float(values[3])])
            # Get all data from polygonal faces
            elif values[0] == 'f':
                for i in range(1, 4):
                    # Get data for vertex i (i = 1, 2, 3)
                    triangle_point_data = values[i]

                    # Separate data
                    if has_normals:
                        position_index, uv_index, normal_index = triangle_point_data.split("/")
                        normal = normal_list[int(normal_index) - 1]
                        vertex_normal_data += [normal[0], normal[1], normal[2]]
                    else:
                        position_index, uv_index = triangle_point_data.split("/")

                    # Add data to corresponding lists
                    position = position_list[int(position_index) - 1]
                    vertex_position_data += [position[0], position[1], position[2]]

                    uv = uv_list[int(uv_index) - 1]
                    vertex_uv_data += [uv[0], uv[1]]

        self.add_attribute("vec3", "vertex_position", vertex_position_data)
        self.add_attribute("vec2", "vertex_uv", vertex_normal_data)
        
        if has_normals:
            self.add_attribute("vec3", "vertex_normal", vertex_normal_data)

        self.vertex_count = len(vertex_position_data)
