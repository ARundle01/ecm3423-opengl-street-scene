import pygame
from texture.texture import Texture
from OpenGL.GL import *
from texture.image_wrapper import ImageWrapper


class CubeMapTexture(Texture):
    """
    Creates a cube-map texture based on 6 given images
    """
    def __init__(self, file_names=None, folder_route=None, target=GL_TEXTURE_CUBE_MAP, properties={}):
        """
        Creates a cubemap texture for use in environment mapping and skyboxes
        :param file_names: file names in order [x-, x+, y-, y+, z-, z+]
        :param folder_route: route to files
        :param target: defaults to GL_TEXTURE_CUBE_MAP
        :param properties:
        """
        self.surface = None
        self.target = target
        self.format = GL_RGB

        # Default property values
        self.properties = {
            "mag_filter": GL_LINEAR,
            "min_filter": GL_LINEAR,
            "wrap": GL_CLAMP_TO_EDGE
        }

        self.set_properties(properties)

        # If no file names are supplied, use a default
        if file_names is None:
            self.file_names = [
                "right.jpg",
                "left.jpg",
                "bottom.jpg",
                "top.jpg",
                "back.jpg",
                "front.jpg"
            ]
        else:
            self.file_names = file_names

        # If the folder is not specified, assume use of ../images
        if folder_route is None:
            self.folder_route = "../images"
        else:
            self.folder_route = folder_route

        # Create and bind to a texture
        self.texture_ref = glGenTextures(1)
        self.bind(target=self.target)

        # Load all 6 images and send to each face of the cubemap
        for i in range(6):
            image = ImageWrapper(file_route=f"{self.folder_route}/{self.file_names[i]}", img_format=self.format)
            if image:
                width = image.get_width()
                height = image.get_height()
                data = image.data()

                glTexImage2D(
                    GL_TEXTURE_CUBE_MAP_POSITIVE_X + i,
                    0,
                    self.format,
                    width,
                    height,
                    0,
                    self.format,
                    GL_UNSIGNED_BYTE,
                    data
                )
            else:
                print(f"Failed to load image texture: {self.folder_route}/{self.file_names[i]}")

        glTexParameteri(self.target, GL_TEXTURE_MAG_FILTER, self.properties["mag_filter"])
        glTexParameteri(self.target, GL_TEXTURE_MIN_FILTER, self.properties["min_filter"])

        glTexParameteri(self.target, GL_TEXTURE_WRAP_S, self.properties["wrap"])
        glTexParameteri(self.target, GL_TEXTURE_WRAP_T, self.properties["wrap"])
        glTexParameteri(self.target, GL_TEXTURE_WRAP_R, self.properties["wrap"])

        self.unbind(target=self.target)
