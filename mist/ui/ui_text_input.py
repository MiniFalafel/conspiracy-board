import pygame

from mist.util import *
from mist.ui import UIElement
from mist.ui import MouseBoxCollider

class UITextInputElement (UIElement):
    def __init__(self, pos: vec2, size: vec2, font_size: int, initial_text: str = ""):
        super().__init__()

        # Create collider to store pos and s
        self.collider = MouseBoxCollider(pos, size)

        # State
        self.active = False
        self.color = (0, 0, 0)

        # Create text objects
        self.text = initial_text
        self.font_size = font_size
        self.font = pygame.font.Font(None, self.font_size)
        self.text_surface = pygame.Surface(self.collider.get_size().elements, pygame.SRCALPHA, 32)
        # Cursor
        self.cursor = pygame.rect.Rect(0, 0, 3, self.font_size)
        self.cursor_index = len(self.text)

    # SETTERS/GETTERS
    def set_pos(self, pos: vec2):
        self.collider.pos = pos

    def set_color(self, color: tuple[int, int, int] | pygame.color.Color):
        self.color = color
        self.__update_text()

    def get_pos(self) -> vec2:
        return self.collider.pos

    def get_size(self) -> vec2:
        return self.collider.get_size()

    def is_active(self):
        return self.active

    # text update
    def __update_text(self):
        # Empty the surface
        self.text_surface = pygame.Surface(self.collider.get_size().elements, pygame.SRCALPHA, 32)
        self.text_surface = self.text_surface.convert_alpha()

        # MANUAL TEXT DRAW
        offset = vec2(0, 0)
        newline_size = self.font.size("X")[1]
        space_size = self.font.size(" ")[0]
        for word in self.text.split(" "):
            # extra variables teehee
            s = self.font.size(word)
            has_newline = False
            if len(word) != 0:
                # If it has a newline at the end, cut it off
                if word[-1] == '\n':
                    word = word[:-1]
                    has_newline = True

                # Check if it'll fit within the boundary on the x-axis
                if s[0] + offset[0] > self.get_size()[0]:
                    # reset offset x and add a newline
                    offset[0] = 0
                    offset[1] += newline_size
                # RENDER
                image = self.font.render(word, True, self.color)

                self.text_surface.blit(image, offset.elements)

            # Increment offset to prepare for next word
            offset[0] += s[0] + space_size
            if has_newline:
                offset[1] += newline_size

    def __clamp_cursor(self):
        self.cursor_index = max(0, min(self.cursor_index, len(self.text)))

    def mouse_button_event(self, button, mouse_pos: vec2, is_down: bool) -> bool:
        # Left Click
        if button == 1 and is_down:
            # Check mouse to collider collision
            collided = self.collider.check_collision(mouse_pos)
            if collided:
                # Grab focus, set active
                self.active = True
                return True
            else:
                # Un-focus
                self.active = False
        return False

    def keyboard_type_event(self, key, char: str) -> bool:
        if self.active:
            # Check if the key is backspace
            if key == pygame.K_BACKSPACE:
                if self.cursor_index > 0:
                    # Backspace the text from the cursor pos
                    new_text = list(self.text)
                    new_text.pop(self.cursor_index - 1) # TODO: Check that this removes the correct character
                    self.text = "".join(new_text)
                    self.cursor_index -= 1 # decrement cursor index
            # Cursor movement
            elif key == pygame.K_LEFT:
                self.cursor_index -= 1
            elif key == pygame.K_RIGHT:
                self.cursor_index += 1
            # Otherwise, type the char
            else:
                # Insert char in at the cursor index
                new_text = list(self.text)
                new_text.insert(self.cursor_index, char)
                self.text = "".join(new_text)
                # Increment cursor pos
                self.cursor_index += 1
            # Update text and cursor
            self.__update_text()
            self.__clamp_cursor()
            # return
            return True
        # Not in focus
        return False

    def on_event(self, event) -> bool:
        # Dispatch the event
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                return self.mouse_button_event(event.button, vec2(*pygame.mouse.get_pos()), True)
            case pygame.MOUSEBUTTONUP:
                return self.mouse_button_event(event.button, vec2(*pygame.mouse.get_pos()), False)
            case pygame.KEYDOWN:
                return self.keyboard_type_event(event.key, event.unicode)

    def draw(self, surface: pygame.Surface):
        # Draw text
        surface.blit(self.text_surface, self.get_pos().elements)

