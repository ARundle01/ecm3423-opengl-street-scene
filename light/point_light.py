from light.light import Light


class PointLight(Light):
    """
    A Light object with colour, position and attenuation
    """
    def __init__(self, colour=[1, 1, 1], position=[0, 0, 0], attenuation=[1, 0, 0.1]):
        """
        Creates a light with colour and attenuation at a position
        :param colour: RGB colour of light
        :param position: world position of light
        :param attenuation: attenuation coefficient for light
        """
        super().__init__(Light.POINT)
        self.colour = colour
        self.set_position(position)
        self.attenuation = attenuation
