import pygame
from OpenGL.GL import *


class ImageWrapper:
    """
    Creates a wrapper to load and deal with a given image
    """
    def __init__(self, file_route, img_format):
        """
        Creates a wrapper to load and parse image
        :param file_route: route to image file
        :param img_format: colour format of image
        """
        print(f"Loading image from: {file_route}")
        self.format = img_format
        self.image = pygame.image.load(file_route)

    def flip(self):
        """
        Flips an image vertically
        """
        self.image = pygame.transform.flip(self.image, False, True)

    def get_width(self):
        """
        Returns the width of the image
        :return: width of the image
        """
        return self.image.get_width()

    def get_height(self):
        """
        Returns the height of the image
        :return: height of the image
        """
        return self.image.get_height()

    def data(self, img_format=GL_RGB):
        """
        Returns the data within an image as a byte string
        :param img_format: colour format of image
        :return: byte string of image
        """
        if img_format == GL_RGBA:
            return pygame.image.tostring(self.image, "RGBA", 1)
        elif img_format == GL_RGB:
            return pygame.image.tostring(self.image, "RGB", 1)
        else:
            raise Exception(f"Unsupported image format: {img_format}")
