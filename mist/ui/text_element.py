import pygame

from mist.ui.ui_element import UIElement
from mist.util.math_types import vec2
from mist.ui.mouse_collider import MouseBoxCollider

class UITextElement (UIElement):
    def __init__(self, pos: vec2, size: vec2, font_size: int, initial_text: str = ""):
        super().__init__()

        # Create collider to store pos and s
        self.collider = MouseBoxCollider(pos, size)

        # State
        self.active = False
        self.color = (0, 0, 0)

        # Create text objects
        self.text_string = initial_text
        self.font_size = font_size
        self.font = pygame.font.Font(None, self.font_size)
        self.text = self.font.render(self.text_string, True, self.color)