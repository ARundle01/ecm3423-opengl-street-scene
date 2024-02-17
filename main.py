# Import core classes
from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh

# Import geometry classes
from geometry.obj_geometry import OBJGeometry
from geometry.box_geometry import BoxGeometry

# Import light classes
from light.ambient_light import AmbientLight
from light.directional_light import DirectionalLight
from light.point_light import PointLight

# Import material classes
from material.cubemap_material import CubeMapMaterial
from material.environment_map_material import EnvironmentMapMaterial
from material.phong_material import PhongMaterial
from material.lambert_material import LambertMaterial
from material.texture_material import TextureMaterial

# Import texture classes
from texture.texture import Texture
from texture.cubemap_texture import CubeMapTexture

# Import movement class
from movement.movement_rig import MovementRig

# Import OpenGL.GL functions
from OpenGL.GL import *

# Import Math functions
from math import pi


class Main(Base):
    def initialise(self):
        """
        Creates a class extended the Base program class, creating the street scene
        """
        print("Initialising program...")

        # Initialise renderer, scene tree and camera with aspect ratio 1920:1000
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=1920 / 1000)

        # Initialise a movement rig and attach the camera
        print("Initialising camera rig...")
        self.rig = MovementRig(degrees_per_sec=30)
        self.rig.add(self.camera)
        self.scene.add(self.rig)
        # Set the starting position and direction
        self.rig.set_position([-11, 2, 0])
        self.rig.set_direction([1, 0, 0])

        # Initialise the sky box using supplied textures
        print("Initialising skybox...")
        self.cube_map = CubeMapTexture(
            file_names=[
                "nx.png",
                "px.png",
                "ny.png",
                "py.png",
                "nz.png",
                "pz.png"
            ],
            folder_route="images/field_skybox"
        )
        # Create skybox with area 1000^2
        sky_box_geo = BoxGeometry(width=1000, height=1000, depth=1000)
        sky_box_mat = CubeMapMaterial(self.cube_map)
        sky_box = Mesh(sky_box_geo, sky_box_mat)
        self.scene.add(sky_box)

        # Initialise the lighting components - 1 ambient light and 1 directional light
        print("Initialising ambient light...")
        ambient = AmbientLight(colour=[0.1, 0.1, 0.1])
        self.scene.add(ambient)

        print("Initialising directional sunlight...")
        # Directional light uses RGB colour mimicking afternoon sunlight
        directional = DirectionalLight(
            colour=[1, 0.839, 0.666], direction=[-1, -1, -2]
        )
        self.scene.add(directional)

        # create all objects in scene
        print("Initialising floor plane...")
        # Add Grass floor
        self.add_floor(width=100, height=100, colour=[0.250, 0.584, 0.239])

        # Add road floor
        self.add_floor(width=100, height=3.8, colour=[0.352, 0.337, 0.305], position=[0, 0.001, 0])
        # Add road marking
        self.add_floor(width=100, height=0.1, colour=[1, 1, 1], position=[0, 0.002, 0])

        # Add pavements
        self.add_floor(width=100, height=0.6, colour=[0.886, 0.882, 0.878], position=[0, 0.001, -2.4])
        self.add_floor(width=100, height=0.6, colour=[0.886, 0.882, 0.878], position=[0, 0.001, 2.4])

        # Add car model using metal texture
        print("Initialising cars...")
        self.add_car(position=[5.25, 0.05, -0.95], texture="images/metal.jpg", rotation=[0, 90, 0], scale=0.26,
                     body_colour=[0.6, 0.2, 0.2])

        # Add tree models along road
        print("Initialising trees...")
        # Negative z side of road
        self.add_tree(position=[-2.625, 0, -2], scale=0.1, rotation=[0, 90, 0], leaf_colour=[0.921, 0.698, 0])
        self.add_tree(position=[2.625, 0, -2], scale=0.1, leaf_colour=[1, 0.470, 0.019])
        self.add_tree(position=[0, 0, -2], scale=0.1, leaf_colour=[0.803, 0.149, 0.074], rotation=[0, 180, 0])

        # Positive z side of road
        self.add_tree(position=[-2.625, 0, 2], scale=0.1, rotation=[0, -90, 0], leaf_colour=[0.921, 0.698, 0])
        self.add_tree(position=[2.625, 0, 2], scale=0.1, leaf_colour=[0.803, 0.149, 0.074], rotation=[0, 180, 0])
        self.add_tree(position=[5.25, 0, 2], scale=0.1, leaf_colour=[1, 0.470, 0.019], rotation=[0, 180, 0])
        self.add_tree(position=[-5.25, 0, 2], scale=0.1, leaf_colour=[0.803, 0.149, 0.074], rotation=[0, 180, 0])

        # Add lamp-post models along road
        print("Initialising lamp-posts...")
        # Negative z side of road
        self.add_lamp_post(position=[5.25, 0, -2], scale=0.5, rotation=[0, -90, 0],
                           lamp_colour=[1, 0.980, 0.956], reflectivity=0.4, attenuation=[1, 0, 0.1])
        self.add_lamp_post(position=[-5.25, 0, -2], scale=0.5, rotation=[0, -90, 0],
                           lamp_colour=[1, 0.980, 0.956], reflectivity=0.4, attenuation=[1, 0, 0.1])

        # Positive z side of road
        self.add_lamp_post(position=[0, 0, 2], scale=0.5, rotation=[0, 90, 0],
                           lamp_colour=[1, 0.980, 0.956], reflectivity=0.4, attenuation=[1, 0, 0.1])

        # Add buildings
        print("Initialising buildings...")
        # Negative z side of road
        self.add_building(position=[5.25, 0, -5])
        self.add_building(position=[-5.25, 0, -5])
        self.add_building(brick_colour=[0.949, 0.905, 0.749], position=[0, 0, -5])

        # Positive z side of road
        self.add_building(position=[5.25, 0, 5])
        self.add_building(position=[-5.25, 0, 5])
        self.add_building(brick_colour=[0.949, 0.905, 0.749], position=[0, 0, 5])

        print("Initialisation complete!\nRunning program...")

    def update(self):
        """
        Updates the render
        """
        # Register input to rig on each iteration of main loop
        self.rig.update(self.input, 1 / 60)

        # Reset camera direction
        if self.input.is_key_down("r"):
            direction = self.rig.get_direction()
            self.rig.set_direction([direction[0], 0, direction[2]])

        # Camera position 1 - Looking down street
        if self.input.is_key_down("1"):
            print("Moving to Camera Position 1...")
            self.rig.set_position([-11, 2, 0])
            self.rig.set_direction([1, 0, 0])

        # Camera position 2 - Looking up street
        if self.input.is_key_down("2"):
            print("Moving to Camera Position 2...")
            self.rig.set_position([11, 2, 0])
            self.rig.set_direction([-1, 0, 0])

        # Register car movement
        if self.input.is_key_pressed("i"):
            for mesh in self.whole_car:
                mesh.translate(0, 0, -1/7.5)
        if self.input.is_key_pressed("k"):
            for mesh in self.whole_car:
                mesh.translate(0, 0, 1/7.5)
        if self.input.is_key_pressed("j"):
            for mesh in self.whole_car:
                mesh.rotate_y(2*pi/180)
        if self.input.is_key_pressed("l"):
            for mesh in self.whole_car:
                mesh.rotate_y(-2*pi/180)

        # Reset car position and direction
        if self.input.is_key_down("backspace"):
            for mesh in self.whole_car:
                mesh.set_position([5.25, 0.05, -0.95])

        # Render scene using camera
        self.renderer.render(self.scene, self.camera)

    @staticmethod
    def set_pos_rot_scale(position, rotation, scale, meshes):
        """
        Sets the position, rotation and scale of the given meshes
        :param position: [x, y, z]
        :param rotation: [x, y, z] in degrees
        :param scale: scaling coefficient
        :param meshes: list of meshes to be set
        """
        for mesh in meshes:
            mesh.set_position(position)
            mesh.rotate_x(rotation[0] * pi / 180)
            mesh.rotate_y(rotation[1] * pi / 180)
            mesh.rotate_z(rotation[2] * pi / 180)
            mesh.scale(scale)

    def add_to_scene(self, meshes):
        """
        Adds a list of meshes to the scene
        :param meshes: List of meshes
        """
        for mesh in meshes:
            self.scene.add(mesh)

    def add_car(self, body_colour=[1, 0, 0], window_colour=[0.815, 0.858, 0.843], wheel_colour=[0.25, 0.25, 0.25],
                reflectivity=0.6, position=[0, 0, 0], rotation=[0, 0, 0], scale=1, texture=None):
        """
        Imports the three car models into meshes and adds them into the scene
        :param body_colour: The RGB colour used by the body of the car
        :param window_colour: The RGB colour used by the windows of the car
        :param wheel_colour: RGB colour used by the wheels of the car
        :param reflectivity: The reflectivity coefficient used in environment mapping on the windows
        :param position: The world position of the model
        :param rotation: The local rotation of the model
        :param scale: The scale of the model
        """
        # Import the car, wheels and window OBJs and create meshes
        car_geo = OBJGeometry(file_name="Car.obj", has_normals=True)
        if texture is not None:
            car_mat = PhongMaterial(texture=Texture(texture), properties={"base_colour": body_colour})
        else:
            car_mat = PhongMaterial(properties={"base_colour": body_colour})
        car_mesh = Mesh(car_geo, car_mat)

        wheels_geo = OBJGeometry(file_name="Car_wheels.obj", has_normals=True)
        wheels_mat = PhongMaterial(properties={"base_colour": wheel_colour})
        wheels_mesh = Mesh(wheels_geo, wheels_mat)

        window_geo = OBJGeometry(file_name="Car_windows.obj", has_normals=True)
        window_mat = EnvironmentMapMaterial(
            enviro_map=self.cube_map,
            properties={"base_colour": window_colour, "reflectivity": reflectivity}
        )
        window_mesh = Mesh(window_geo, window_mat)

        # Allow the 3 meshes to be used by the class
        self.whole_car = [car_mesh, wheels_mesh, window_mesh]

        self.set_pos_rot_scale(
            position=position,
            rotation=rotation,
            scale=scale,
            meshes=self.whole_car
        )

        # add all to the scene
        self.add_to_scene(meshes=self.whole_car)

    def add_tree(self, trunk_colour=[0.458, 0.384, 0.266], leaf_colour=[0.301, 0.549, 0.341], position=[0, 0, 0],
                 rotation=[0, 0, 0], scale=1, leaf_texture=None, trunk_texture=None):
        """
        Imports the two tree models into meshes and adds them into the scene
        :param trunk_colour: RGB colour for the trunk
        :param leaf_colour: RGB colour for the leaves
        :param position: World position
        :param rotation: Local rotation
        :param scale: Scale
        :param leaf_texture: Optional leaf texture
        :param trunk_texture: Optional trunk texture
        """
        # Import trunk and leaf models, using textures if supplied
        trunk_geo = OBJGeometry(file_name="tree_trunk.obj", has_normals=True)
        if trunk_texture is not None:
            trunk_mat = LambertMaterial(texture=Texture(trunk_texture))
        else:
            trunk_mat = LambertMaterial(properties={"base_colour": trunk_colour})
        trunk_mesh = Mesh(trunk_geo, trunk_mat)

        leaf_geo = OBJGeometry(file_name="tree_leaves.obj", has_normals=True)
        if leaf_texture is not None:
            leaf_mat = LambertMaterial(texture=Texture(leaf_texture))
        else:
            leaf_mat = LambertMaterial(properties={"base_colour": leaf_colour})
        leaf_mesh = Mesh(leaf_geo, leaf_mat)

        # Set position, rotation and scale of both meshes simultaneously
        self.set_pos_rot_scale(
            position=position,
            rotation=rotation,
            scale=scale,
            meshes=[trunk_mesh, leaf_mesh]
        )
        # Add to scene
        self.add_to_scene(meshes=[trunk_mesh, leaf_mesh])

    def add_building(self, brick_colour=[0.862, 0.333, 0.223], bevel_colour=[0.619, 0.592, 0.576], position=[0, 0, 0],
                     rotation=[0, 0, 0], scale=1, reflectivity=0.6, window_colour=[0.815, 0.858, 0.843]):
        """
        Imports the three building models into meshes and adds them into the scene
        :param brick_colour: RGB colour for bricks
        :param bevel_colour: RGB colour for bevelled parts
        :param position: World position
        :param rotation: Local rotation
        :param scale: Scale
        :param reflectivity: Reflectivity of windows
        :param window_colour: RGB colour for window
        """
        # Import bevel, body and window models
        bevel_geo = OBJGeometry(file_name="building_bevel.obj", has_normals=True)
        bevel_mat = LambertMaterial(properties={"base_colour": bevel_colour})
        bevel_mesh = Mesh(bevel_geo, bevel_mat)

        body_geo = OBJGeometry(file_name="building_body.obj", has_normals=True)
        body_mat = LambertMaterial(properties={"base_colour": brick_colour})
        body_mesh = Mesh(body_geo, body_mat)

        windows_geo = OBJGeometry(file_name="building_windows.obj", has_normals=True)
        # Create environment mapped reflections
        windows_mat = EnvironmentMapMaterial(
            enviro_map=self.cube_map,
            properties={"base_colour": window_colour, "reflectivity": reflectivity}
        )
        windows_mesh = Mesh(windows_geo, windows_mat)

        # Set the position, rotation and scale
        self.set_pos_rot_scale(
            position=position,
            rotation=rotation,
            scale=scale,
            meshes=[bevel_mesh, body_mesh, windows_mesh]
        )
        # Add to the scene
        self.add_to_scene(meshes=[bevel_mesh, body_mesh, windows_mesh])

    def add_floor(self, colour=[0, 0, 0], width=1, height=1, position=[0, 0, 0], rotation=[0, 0, 0], scale=1,
                  texture=None):
        """
        Create floor objects (such as road, pavement)
        :param colour: RGB colour of floor
        :param width: width of floor in z-direction
        :param height: depth of floor in x-direction
        :param position: World position
        :param rotation: Local rotation
        :param scale: Scale
        :param texture: Optional texture to use
        """
        # Create a box of width by height by 0.1
        floor_geo = BoxGeometry(width=width, depth=height, height=0.1)
        # Apply texture if supplied
        if texture is not None:
            floor_mat = TextureMaterial(
                texture=Texture(texture, properties={"wrap": GL_REPEAT})
            )
        else:
            floor_mat = LambertMaterial(
                properties={"base_colour": colour}
            )
        floor_mesh = Mesh(floor_geo, floor_mat)
        # Set position, rotation and scale
        self.set_pos_rot_scale(
            position=position,
            rotation=rotation,
            scale=scale,
            meshes=[floor_mesh]
        )
        # Add to scene
        self.add_to_scene(meshes=[floor_mesh])

    def add_lamp_post(self, position=[0, 0, 0], rotation=[0, 0, 0], scale=1, pole_colour=[0, 0, 0],
                      lamp_colour=[0.905, 0.650, 0.207], reflectivity=0.6, attenuation=[1, 0, 1]):
        """
        Imports two lamp-post models into meshes, creates a point light and adds them to scene
        :param position: World position
        :param rotation: Local rotation
        :param scale: Scale
        :param pole_colour: RGB colour of pole
        :param lamp_colour: RGB colour of lamp
        :param reflectivity: Reflectivity of pole
        :param attenuation: Attenuation of point light
        """
        # Import pole and lamp models
        pole_geo = OBJGeometry(file_name="pole.obj")
        pole_mat = EnvironmentMapMaterial(
            enviro_map=self.cube_map,
            properties={"base_colour": pole_colour, "reflectivity": reflectivity}
        )
        pole_mesh = Mesh(pole_geo, pole_mat)

        lamp_geo = OBJGeometry(file_name="lamp.obj")
        lamp_mat = PhongMaterial(properties={"base_colour": lamp_colour})
        lamp_mesh = Mesh(lamp_geo, lamp_mat)
        # Create a point light
        light = PointLight(colour=lamp_colour, position=position, attenuation=attenuation)
        # Add light to scene
        self.scene.add(light)
        # Set position, rotation and scale of meshes
        self.set_pos_rot_scale(
            position=position,
            rotation=rotation,
            scale=scale,
            meshes=[pole_mesh, lamp_mesh]
        )
        # Add meshes to scene
        self.add_to_scene(meshes=[pole_mesh, lamp_mesh])


if __name__ == '__main__':
    # Run the main class with screen size 1920x1000
    Main(screen_size=[1920, 1000]).run()
