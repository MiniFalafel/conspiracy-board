from mist.ui.ui_element import UIDragSprite, vec2
from mist.ui.sprite import Sprite

class StickyNote (UIDragSprite):
    def __init__(self, pos: vec2, sprite_path: str, size: int, click_padding: int = 0):
        super().__init__(pos, sprite_path, vec2(size, size), click_padding)
        GRAB_SCALE_OFFSET = 6
        self.grabbed_offset = vec2(GRAB_SCALE_OFFSET // 2, GRAB_SCALE_OFFSET // 2)
        self.grabbed_sprite = Sprite(sprite_path, vec2(size + GRAB_SCALE_OFFSET, size + GRAB_SCALE_OFFSET))

    def draw(self, surface):
        # Choose sprite based on is_pinned()
        s = self.sprite
        s_pos = self.get_sprite_pos()
        if self.is_pinned():
            s = self.grabbed_sprite
            s_pos -= self.grabbed_offset
        # Draw
        s.draw(surface, s_pos)

