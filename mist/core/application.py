import pygame.event

from mist.core.window import Window
from mist.core.layer import LayerStack
from mist.core.clock import Clock

class Application:
    # Static instance (singleton!!)
    __s_Instance = None

    # Mouse pos
    last_frame_mouse_pos = [0, 0]

    def __init__(self, width: int = 800, height: int = 600, title: str = "Application"):

        # Make sure that an application hasn't already been created
        if Application.__s_Instance is not None:
            raise Exception("APPLICATION ALREADY INITIALIZED! You can only have one application instance per program.")

        # Init pygame
        pygame.init()

        # Create a window object
        self.window = Window(width, height, title)

        # Layer Stack
        self.layer_stack = LayerStack()

        # State stuff
        self.running = False
        self.clock = pygame.time.Clock()
        self.last_frame_dt = 0
        self.tick_rate = 60

    def __quit(self):
        self.running = False

    @staticmethod
    def get_last_frame_mouse_pos():
        return Application.last_frame_mouse_pos

    def run(self):
        # Set running to true
        self.running = True

        while self.running:

            # Dispatch all events
            for event in pygame.event.get():
                match event.type:
                    # If a quit event is called, make sure to end all application processes.
                    case pygame.QUIT:
                        self.__quit()
                # Pass event to layers
                self.layer_stack.on_event(event)

            # Update Layer Stack
            self.layer_stack.update()

            # Render the layers
            self.layer_stack.render(self.window.data.native_window)

            # Update pygame window
            self.window.update()
            self.window.data.native_window.fill((12, 25, 25))

            # Update clock
            self.last_frame_dt = self.clock.tick(self.tick_rate)
            # Update the static clock
            Clock.update(self.last_frame_dt / 1000.0)
            # UPDATE MOUSE
            Application.last_frame_mouse_pos = pygame.mouse.get_pos()

        # END OF RUN

