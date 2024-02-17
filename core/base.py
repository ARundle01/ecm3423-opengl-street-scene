import pygame
import sys
from core.input import Input


class Base(object):
    """
    Base model class, all other models will inherit from this
    """
    def __init__(self, screen_size=[768, 768]):
        # Initialise pygame modules
        pygame.init()

        # Set screen size to 768x768, with Double Buffering and using OpenGL
        screen_size = screen_size
        display_flags = pygame.DOUBLEBUF | pygame.OPENGL

        # Enable 4x Antialiasing
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        self.screen = pygame.display.set_mode(screen_size, display_flags)

        # Enable cross-OS compatability
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK,
                                        pygame.GL_CONTEXT_PROFILE_CORE)

        # Set window name
        pygame.display.set_caption("Street Scene")

        # Set running flag
        self.running = True
        # Initialise clock
        self.clock = pygame.time.Clock()
        # Take any inputs to the window
        self.input = Input()

    def initialise(self):
        """
        Base method to be overloaded later by model classes
        """
        pass

    def update(self):
        """
        Base method to be overloaded later by model classes
        """
        pass

    def run(self):
        """
        Renders scene
        """
        self.initialise()

        # main loop
        while self.running:
            # process input
            self.input.update()
            if self.input.quit:
                self.running = False

            # update
            self.update()

            # render
            pygame.display.flip()

            # make 60 FPS
            self.clock.tick(60)

        # shutdown
        pygame.quit()
        sys.exit()
