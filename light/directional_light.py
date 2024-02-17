from light.light import Light


class DirectionalLight(Light):
    """
    A light object with colour and direction
    """
    def __init__(self, colour=[1, 1, 1], direction=[0, -1, 0]):
        """
        Creates a light with colour and direction
        :param colour: RGB colour of light
        :param direction: direction of light
        """
        super().__init__(Light.DIRECTIONAL)
        self.colour = colour
        self.set_direction(direction)
