from core.object3d import Object3D
from math import pi


class MovementRig(Object3D):
    """
    Specifies a movable Object3D, to which other Object3Ds can be attached
    """
    def __init__(self, units_per_sec=1, degrees_per_sec=60):
        super().__init__()

        # Initialise attached Object3D
        self.look_attachment = Object3D()
        self.children = [self.look_attachment]
        self.look_attachment.parent = self

        # Store parameters
        self.units_per_sec = units_per_sec
        self.degrees_per_sec = degrees_per_sec

        # Set Keymappings for first person camera
        self.KEY_MOVE_FORWARD = "w"
        self.KEY_MOVE_BACK = "s"
        self.KEY_MOVE_LEFT = "a"
        self.KEY_MOVE_RIGHT = "d"

        self.KEY_MOVE_UP = "space"
        self.KEY_MOVE_DOWN = "left shift"

        self.KEY_TURN_LEFT = "left"
        self.KEY_TURN_RIGHT = "right"
        self.KEY_LOOK_UP = "up"
        self.KEY_LOOK_DOWN = "down"

    def add(self, child):
        """
        Adds a child object to the movement rig
        :param child:
        :return:
        """
        self.look_attachment.add(child)

    def update(self, input_object, delta_time):
        """
        Updates the movement rig based on some input
        :param input_object: object supplying input
        :param delta_time: the rate at which movement rig is being updated
        """
        move_amount = self.units_per_sec * delta_time
        rotate_amount = self.degrees_per_sec * pi/180 * delta_time

        # Check movement inputs
        if input_object.is_key_pressed(self.KEY_MOVE_FORWARD):
            self.translate(0, 0, -move_amount)
        if input_object.is_key_pressed(self.KEY_MOVE_BACK):
            self.translate(0, 0, move_amount)
        if input_object.is_key_pressed(self.KEY_MOVE_LEFT):
            self.translate(-move_amount, 0, 0)
        if input_object.is_key_pressed(self.KEY_MOVE_RIGHT):
            self.translate(move_amount, 0, 0)
        if input_object.is_key_pressed(self.KEY_MOVE_UP):
            self.translate(0, move_amount, 0)
        if input_object.is_key_pressed(self.KEY_MOVE_DOWN):
            self.translate(0, -move_amount, 0)

        # Check turning inputs
        if input_object.is_key_pressed(self.KEY_TURN_LEFT):
            self.rotate_y(rotate_amount)
        if input_object.is_key_pressed(self.KEY_TURN_RIGHT):
            self.rotate_y(-rotate_amount)

        # Check looking inputs
        if input_object.is_key_pressed(self.KEY_LOOK_UP):
            self.look_attachment.rotate_x(rotate_amount)
        if input_object.is_key_pressed(self.KEY_LOOK_DOWN):
            self.look_attachment.rotate_x(-rotate_amount)
