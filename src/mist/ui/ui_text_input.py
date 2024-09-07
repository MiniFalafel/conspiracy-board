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
        self.text_surface = None
        self.text_surface_size = self.collider.get_size()
        # Cursor
        self.cursor = pygame.Surface((2, self.font.size("|")[1]))
        self.cursor.fill(self.color)
        self.cursor_index = len(self.text)
        self.cursor_pos = vec2(0, 0)
        # Update text display
        self.__update_text()

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

    def __wrap_lines(self, lines: list, wrap_width: int):
        # initialize return
        new_lines = [""]
        # loop through each line
        for line in lines:
            # loop through all the characters
            for char in line:
                # Check the width of the current line if it had this character
                if self.font.size((new_lines[-1] + char))[0] > wrap_width:
                    # too big, start new line
                    # Find last space
                    i = new_lines[-1].rfind(" ")
                    if i == -1:
                        new_lines.append(char)
                    else:
                        # Add whatever's after the space to the new line
                        new_lines.append(new_lines[-1][i + 1:] + char)
                        new_lines[-2] = new_lines[-2][:i]
                else:
                    # not too big, keep adding to this line
                    new_lines[-1] += char
            # start new line
            new_lines.append("")
        # return
        #return new_lines
        # TODO: RE-ENABLE LINE WRAPPING
        return lines

    # text update
    def __update_text(self):
        # MANUAL TEXT DRAW
        # size of each line
        newline_size = self.font.size("X")[1]

        # Split current text into lines
        lines = self.text.replace("\r", "\n").split("\n")
        # wrap the text
        lines = self.__wrap_lines(lines, self.text_surface_size[0])
        # Update cursor
        self.cursor_pos = self.__update_cursor(lines)

        # Update surface size based on number of lines
        self.text_surface_size[1] = len(lines) * newline_size
        # Empty the surface
        self.text_surface = pygame.Surface(self.text_surface_size.elements, pygame.SRCALPHA, 32)
        self.text_surface = self.text_surface.convert_alpha()
        # Loop through lines, render each, and blit to text surface

        for i in range(len(lines)):
            # Don't bother rendering if the line is blank
            if lines[i] == "":
                continue
            # Render the line
            line_img = self.font.render(lines[i], True, self.color)
            # blit to text surface
            self.text_surface.blit(line_img, (0, newline_size * i))

    def cursor_index_to_pos(self, i: int):
        """
        s = "This is a line\n\n\nThere are two empty lines above me!\nASLKJHKJHHFHDDGFFDKSJHF and such\n"
        # IF LINE WRAPPING WAS DISABLED: ---------------
        l = [
            "This is a line",
            "",
            "",
            "There are two empty lines above me!",
            "ASLKJHKJHHFHDDGFFDKSJHF and such",
            "",
        ]

        Since the "newline" ('\n', and '\r') were removed at the ends of all the lines
        """
        pass

    def __update_cursor(self, lines: list):
        # Loop through the lines, checking if any
        #return vec2(self.font.size(self.text[:self.cursor_index])[0], 0)
        ci = 0
        cl = 0
        for line in lines:
            diff = ci + len(line) - self.cursor_index
            if diff < 0:
                ci = -diff
                break
            cl += 1
        return vec2(self.font.size(lines[cl][:ci])[0], cl * self.font.size("X")[1])

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
                # enable key repeating
                pygame.key.set_repeat(750, 50)
                return True
            else:
                # Un-focus
                self.active = False
                # disable key repeating
                pygame.key.set_repeat(0, 0)
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
        # Draw cursor
        if self.active:
            surface.blit(self.cursor, (self.cursor_pos + self.get_pos()).elements)

