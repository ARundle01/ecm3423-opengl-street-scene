from core.object3d import Object3D
from core.matrix import Matrix
from numpy.linalg import inv


class Camera(Object3D):
    """
    Represents camera in scene
    """
    def __init__(self, angle_of_view=60, aspect_ratio=1, near=0.1, far=1000):
        super().__init__()
        # Create projection and view matrix of camera
        self.project_matrix = Matrix.make_perspective(angle_of_view, aspect_ratio, near, far)
        self.view_matrix = Matrix.make_identity()

    def update_view_matrix(self):
        """
        Updates View matrix as needed, doing inverse of world matrix
        """
        self.view_matrix = inv(self.get_world_matrix())
