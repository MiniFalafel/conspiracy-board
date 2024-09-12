import random

from mist import Layer, vec2, Sprite, UITextInputElement
from sticky_note import StickyNote

import pygame

class UIObjectsLayer(Layer):

    def __init__(self):
        super().__init__("UI Objects Layer")

        # Create an array of UI elements
        self.ui_elements = []

        # Render surface
        self.back_buffer = pygame.Surface((1280, 720))
        self.window_size = self.back_buffer.get_size()

        # Corkboard
        self.corkboard = Sprite("res/textures/corkboard.png")

        # Populate
        NUM_ELEMENTS = 3
        sprite_path = "res/textures/sticky_note.png"
        for i in range(NUM_ELEMENTS):
            x, y = [random.randint(0, 400) for i in range(2)]
            self.ui_elements.append(StickyNote(vec2(x, y), sprite_path, 200, -30))

        text = """\
bitch!

you KNOW i'm sexy

UGH!

don't call, just
t e x t m e

bitch I'm slow don't (idk the lyrics)\
        """

        text_el = UITextInputElement(vec2(20, 20), vec2(300, 50), 40, text)
        self.ui_elements.append(text_el)

        # Load sticky note sounds
        pygame.mixer.init()
        StickyNote.load_sound("res/sounds/sticky_note/note_peel.wav")
        StickyNote.load_sound("res/sounds/sticky_note/note_stick.wav", None, 0.5)

    def on_event(self, event) -> bool:
        if event.type == pygame.WINDOWRESIZED:
            self.window_size = event.size
        # Store new array for the list in case the order changed
        new_order = self.ui_elements[:]

        # Keep track of what to return
        r = False

        # Pass event to ui elements
        for i in range(len(self.ui_elements)):
            if self.ui_elements[i].pass_event(event):
                # This element has handled the event, so move it to the top of the list
                el = new_order.pop(i)
                new_order = [el, *new_order] # Move to front
                r = True
                break # Don't let other elements try and handle it if it's already been handled
        # switch out self.ui_elements for new_order
        self.ui_elements = new_order

        # Return
        return r

    def on_render(self, surface):
        # Draw the cork board
        self.corkboard.draw(self.back_buffer, vec2(0, 0))

        # Loop through all ui elements
        for el in reversed(self.ui_elements):
            el.draw(self.back_buffer)

        # Draw back_buffer to surface
        surface.blit(self.back_buffer, (0, 0), pygame.rect.Rect(0, 0, 1280, 720))
