import pygame

class Window:

    # Struct for holding important window information for easy storage.
    class WindowData:
        def __init__(self, width: int, height: int, title: str):
            self.width = width
            self.height = height
            self.title = title
            self.native_window = None

    def __init__(self, width: int, height: int, title: str):
        # Create self.data struct
        self.data = Window.WindowData(width, height, title)

        # Set up pygame window
        self.data.native_window = pygame.display.set_mode((self.data.width, self.data.height))
        pygame.display.set_caption(self.data.title)

    def update(self):
        # Updates pygame window stuff
        pygame.display.flip()

