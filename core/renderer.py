from OpenGL.GL import *
from core.mesh import Mesh
from light.light import Light
import pygame


class Renderer(object):
    def __init__(self, clear_colour=[0, 0, 0]):
        """
        Creates an object to render the scene
        :param clear_colour:
        """
        glEnable(GL_DEPTH_TEST)
        glClearColor(clear_colour[0], clear_colour[1], clear_colour[2], 1.0)

        # Support transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.window_size = pygame.display.get_surface().get_size()

    def render(self, scene, camera):
        """
        Renders the given scene using the given camera
        :param scene: scene to render
        :param camera: camera to render with
        """
        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Update camera view matrix
        camera.update_view_matrix()

        # Extract list of Mesh objects
        descendant_list = scene.get_descendant_list()
        mesh_filter = lambda x: isinstance(x, Mesh)
        mesh_list = list(filter(mesh_filter, descendant_list))

        # Extract list of lights
        light_filter = lambda x: isinstance(x, Light)
        light_list = list(filter(light_filter, descendant_list))
        while len(light_list) < 4:
            light_list.append(Light())

        for mesh in mesh_list:
            # If mesh is not visible, continue
            if not mesh.visible:
                continue

            glUseProgram(mesh.material.program_ref)

            # Bind VAO
            glBindVertexArray(mesh.vao_ref)

            # Update Uniform matrices
            mesh.material.uniforms["model_matrix"].data = mesh.get_world_matrix()
            mesh.material.uniforms["view_matrix"].data = camera.view_matrix
            mesh.material.uniforms["projection_matrix"].data = camera.project_matrix

            # Update light uniforms
            if "light0" in mesh.material.uniforms.keys():
                for light_number in range(4):
                    light_name = "light" + str(light_number)
                    light_object = light_list[light_number]
                    mesh.material.uniforms[light_name].data = light_object

            if "view_position" in mesh.material.uniforms.keys():
                mesh.material.uniforms["view_position"].data = camera.get_world_position()

            # Update all material Uniforms
            for variable_name, uniform_object in mesh.material.uniforms.items():
                uniform_object.upload_data()

            # Update render settings
            mesh.material.update_render_settings()

            # Draw the meshes
            glDrawArrays(mesh.material.settings["draw_style"], 0, mesh.geometry.vertex_count)
