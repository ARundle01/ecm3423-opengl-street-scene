from core.object3d import Object3D


class Light(Object3D):
    """
    Defines a light object, which can be ambient, directional or a point light
    """
    AMBIENT = 1
    DIRECTIONAL = 2
    POINT = 3

    def __init__(self, light_type=0):
        """
        Creates a light
        :param light_type: whether a light is ambient (1), directional (2) or point (3)
        """
        super().__init__()
        self.light_type = light_type
        self.colour = [1, 1, 1]
        self.attenuation = [1, 0, 0]
