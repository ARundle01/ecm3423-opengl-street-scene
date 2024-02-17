import pygame
from OpenGL.GL import *
from texture.image_wrapper import ImageWrapper


class Texture(object):
    def __init__(self, file_name=None, target=GL_TEXTURE_2D, properties={}):
        """
        Creates a 2D texture from a given image
        :param file_name: file name of object
        :param target: OpenGL target of texture
        :param properties: properties of texture (the mag and min filters and the wrap to use)
        """
        # Pygame surface object to store image data
        self.surface = None
        self.target = target

        # Generate texture reference
        self.texture_ref = glGenTextures(1)

        # Default property values
        self.properties = {
            "mag_filter": GL_LINEAR,
            "min_filter": GL_LINEAR_MIPMAP_LINEAR,
            "wrap": GL_REPEAT
        }

        # Override default properties
        self.set_properties(properties)

        if file_name is not None:
            self.load_image(file_name)
            self.upload_data()

    def load_image(self, file_name):
        """
        Load image from directory into a pygame surface
        :param file_name: image file name
        """
        self.surface = ImageWrapper(file_route=file_name, img_format=GL_RGBA)

    def set_properties(self, properties):
        """
        Set properties of texture object
        :param properties: properties to set
        """
        for name, data in properties.items():
            if name in self.properties.keys():
                self.properties[name] = data
            else:
                raise Exception(f"No property named: {name}")

    def upload_data(self, is_render_target=False):
        """
        Upload image data and parameters to texture object, and upload to GPU
        :return:
        """
        width = self.surface.get_width()
        height = self.surface.get_height()

        if is_render_target:
            pixel_data = pygame.image.tostring(self.surface, "RGBA", 1)
        else:
            # Convert image to string buffer
            pixel_data = self.surface.data(self.surface.format)

        # Bind texture
        self.bind(self.target)

        # Send data to texture object
        glTexImage2D(self.target, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixel_data)

        # Generate Mipmaps
        glGenerateMipmap(self.target)

        # Set texture mag and min filters
        glTexParameteri(self.target, GL_TEXTURE_MAG_FILTER, self.properties["mag_filter"])
        glTexParameteri(self.target, GL_TEXTURE_MIN_FILTER, self.properties["min_filter"])

        # Set texture wrap
        glTexParameteri(self.target, GL_TEXTURE_WRAP_S, self.properties["wrap"])
        glTexParameteri(self.target, GL_TEXTURE_WRAP_T, self.properties["wrap"])

    def bind(self, target=GL_TEXTURE_2D):
        """
        Binds a named texture to a texture target - for use in making cubemaps
        """
        glBindTexture(target, self.texture_ref)

    def unbind(self, target=GL_TEXTURE_2D):
        """
        Unbinds a named texture from a texture target
        """
        glBindTexture(target, 0)
