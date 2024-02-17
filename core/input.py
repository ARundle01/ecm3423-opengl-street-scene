import pygame


class Input(object):
    def __init__(self):
        """
        Creates an Input object
        """
        # Check if user has quit application
        self.quit = False

        # Lists of key states
        # down, up press: discrete key presses, lasts 1 iteration
        # pressed: continuous event, lasts from down to up event
        self.key_down_list = []
        self.key_pressed_list = []
        self.key_up_list = []

    def update(self):
        """
        Iterates over all user input events that have occurred
        since last time events were checked
        """
        # Reset discrete key states
        self.key_down_list = []
        self.key_up_list = []

        for event in pygame.event.get():
            # Quit event occurs when pressing button to close window
            if event.type == pygame.QUIT:
                self.quit = True
            # check for key down & up events, append key name to lists
            if event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                self.key_down_list.append(key_name)
                self.key_pressed_list.append(key_name)
            if event.type == pygame.KEYUP:
                key_name = pygame.key.name(event.key)
                self.key_pressed_list.remove(key_name)
                self.key_up_list.append(key_name)

    def is_key_down(self, key_name):
        """
        Check if key is down
        :param key_name: name of key
        :return: bool, dependent on if key is down
        """
        return key_name in self.key_down_list

    def is_key_up(self, key_name):
        """
        Check if key is up
        :param key_name: name of key
        :return: bool, dependent on if key is up
        """
        return key_name in self.key_up_list

    def is_key_pressed(self, key_name):
        """
        Check if key is currently pressed
        :param key_name: name of key
        :return: bool, dependent on if key is pressed
        """
        return key_name in self.key_pressed_list
