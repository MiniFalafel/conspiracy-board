import random

from mist import Layer, vec2
from sticky_note import StickyNote

class UIObjectsLayer(Layer):

    def __init__(self):
        super().__init__("UI Objects Layer")

        # Create an array of UI elements
        self.ui_elements = []

        # Populate
        NUM_ELEMENTS = 3
        sprite_path = "res/textures/sticky_note.png"
        for i in range(NUM_ELEMENTS):
            x, y = [random.randint(0, 400) for i in range(2)]
            self.ui_elements.append(StickyNote(vec2(x, y), sprite_path, 200, -30))

    def on_event(self, event) -> bool:
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
        # Loop through all ui elements
        for el in reversed(self.ui_elements):
            el.draw(surface)