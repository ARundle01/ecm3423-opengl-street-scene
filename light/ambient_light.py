from light.light import Light


class AmbientLight(Light):
    """
    Ambient light has no sense of direction or attenuation, only a colour
    """
    def __init__(self, colour=[1, 1, 1]):
        """
        Creates ambient light with colour
        :param colour: RGB colour of light
        """
        super().__init__(Light.AMBIENT)
        self.colour = colour
