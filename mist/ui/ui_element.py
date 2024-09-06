import pygame

from mist.ui.mouse_collider import MouseCollider, MouseBoxCollider
from mist.util.math_types import vec2
from mist.ui.sprite import Sprite

class UIElement:
    """
    UI Element:
     - Like an empty.
     - Subclasses of this will be the most useful.
    """

    def __init__(self):
        # Create a list of children
        self.children = list()

    # MAIN EVENT PASSING METHOD
    def pass_event(self, event) -> bool:
        # Check if on_event has been implemented
        result = self.on_event(event)
        if result is not None:
            return result
        # Otherwise, not handled
        return False

    # "VIRTUAL" METHODS

    # GETTERS
    def get_collider(self):
        pass

    # SETTERS
    def set_collider(self, collider: MouseCollider):
        pass

    # 'Virtual' CALLBACKS
    def on_event(self, event) -> bool:
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass

# Draggable UI
class UIDraggable (UIElement):
    def __init__(self):
        super().__init__()
        # Collider
        self.collider = None

        # Current state
        self.pin_to_cursor = False
        self.pinned_offset = vec2(0, 0)

    # GETTERS/SETTERS
    def get_collider(self):
        return self.collider

    def set_collider(self, collider: MouseCollider, inherit_pos: bool = True):
        # Check if a collider already exists
        if self.collider is not None:
            # Store old position
            old_coll = self.collider
            # Set the new collider
            self.collider = collider
            # Update new collider to match old collider transform
            if inherit_pos:
                self.collider.pos = old_coll.get_pos()
        else:
            self.collider = collider

    def is_pinned(self) -> bool:
        return self.pin_to_cursor

    # EVENTS
    def mouse_move_event(self, mouse_pos: vec2) -> bool:
        """
        IF - This element should be dragged.
        Adjusts object position to preserve the relative offset between itself and the mouse
        """
        if self.pin_to_cursor:
            # Get new offset
            new_off = self.__offset_from_mouse()
            # Get the difference between the current offset and the pinned offset
            diff = new_off - self.pinned_offset
            # Add diff to the pos
            self.collider.pos += diff

        return False

    def __offset_from_mouse(self) -> vec2:
        # Get relative offset of mousse and element and store it
        return vec2(*pygame.mouse.get_pos()) - self.collider.pos

    def mouse_button_event(self, button, button_down: bool, mouse_pos: vec2) -> bool:
        """
        Checks mouse position on click against the element and its collider.
        """
        # BUTTON PRESSED:
        if button_down:
            # Update self.pin_to_cursor
            if button == 1: # 1 == left click (lame that pygame doesn't define this with an enum imo).
                # Check if the mouse is within the element's collider
                collided = self.collider.check_collision(mouse_pos)
                if collided:
                    self.pin_to_cursor = True
                    # Get relative offset of mousse and element and store it
                    self.pinned_offset = self.__offset_from_mouse()
                    # Call pin callback
                    self.on_pin()
                    return True
        else: # Button release
            if button == 1:
                # Call release callback
                self.on_release()
                # Reset pin_to_cursor
                self.pin_to_cursor = False

        # Only return true if the event is a mouse button press (DOWN). That way nothing gets locked to the mouse on accident later.
        return False

    def on_event(self, event) -> bool:
        """
        Dispatches Mouse events to corresponding functions.
        """
        match event.type:
            case pygame.MOUSEMOTION:
                return self.mouse_move_event(vec2(*pygame.mouse.get_pos()))
            case pygame.MOUSEBUTTONDOWN:
                return self.mouse_button_event(event.button, True, vec2(*pygame.mouse.get_pos()))
            case pygame.MOUSEBUTTONUP:
                return self.mouse_button_event(event.button, False, vec2(*pygame.mouse.get_pos()))

    # 'VIRTUAL' methods for subclasses
    def on_pin(self) -> None:
        """
        A callback - called ONCE when the UI element is clicked on and mouse collision is confirmed.
        """
        pass

    def on_release(self) -> None:
        """
        A callback - called ONCE when the mouse is released and the UI element is no longer locked to the cursor.
        """
        pass

# Draggable Sprite
class UIDragSprite (UIDraggable):
    def __init__(self, pos: vec2, sprite_path: str, sprite_size: vec2, collider_padding: int = 0):
        """

        :param sprite_path: Filepath to the image/texture that will be displayed at the element's position
        :param pos: The starting position of the UI element
        :param sprite_size: A vec2() that indicates the x and y size in pixels that the sprite should display as
        :param collider_padding: How many pixels larger than the image is the collider? Can be negative for a collider which is smaller than the sprite image
        """
        super().__init__()

        # Setup collider with dimensions
        self.collider_offset = vec2(-collider_padding, -collider_padding)
        collider_size = vec2(sprite_size[0] + 2 * collider_padding, sprite_size[1] + 2 * collider_padding)
        # Create the collider and set it
        coll = MouseBoxCollider(pos + self.collider_offset, collider_size)
        self.set_collider(coll)

        # Load Sprite
        self.sprite = Sprite(sprite_path, sprite_size)

    def set_pos(self, pos: vec2):
        self.collider.pos = pos + self.collider_offset

    def get_sprite_pos(self):
        return self.collider.pos - self.collider_offset

    def get_collider_pos(self):
        return self.collider.pos

    def draw(self, surface):
        self.sprite.draw(surface, self.get_sprite_pos())

        # DEBUG DRAW COLLIDER BOUNDS
        #pygame.draw.rect(surface, (255, 0, 0), (*self.collider.pos.elements, *self.collider.dim), 2)

    def update(self):
        self.sprite.update()
