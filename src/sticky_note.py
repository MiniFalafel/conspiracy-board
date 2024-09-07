import pygame.mixer

from mist.ui.ui_element import UIDragSprite, vec2
from mist.ui.sprite import Sprite
from mist.util.log import Log

class StickyNote (UIDragSprite):

    s_SoundBank = {
        "note_peel": None,
        "note_stick": None,
    }

    def __init__(self, pos: vec2, sprite_path: str, size: int, click_padding: int = 0):
        super().__init__(pos, sprite_path, vec2(size, size), click_padding)
        GRAB_SCALE_OFFSET = 6
        self.grabbed_offset = vec2(GRAB_SCALE_OFFSET // 2, GRAB_SCALE_OFFSET // 2)
        self.grabbed_sprite = Sprite(sprite_path, vec2(size + GRAB_SCALE_OFFSET, size + GRAB_SCALE_OFFSET))

    @staticmethod
    def load_sound(path: str, name: str = None, mix_level: float = 1.0):
        # Load the sound using pygame
        sound = pygame.mixer.Sound(path)
        sound.set_volume(mix_level)
        # Get the name
        name_ = name
        if name is None:
            i0 = path.rfind("/")
            i1 = path.rfind(".")
            name_ = path[i0+1:i1]
        # Add it to the sound bank
        StickyNote.s_SoundBank[name_] = sound

    def draw(self, surface):
        # Choose sprite based on is_pinned()
        s = self.sprite
        s_pos = self.get_sprite_pos()
        if self.is_pinned():
            s = self.grabbed_sprite
            s_pos -= self.grabbed_offset
        # Draw
        s.draw(surface, s_pos)

    def on_pin(self) -> None:
        sound = StickyNote.s_SoundBank["note_peel"]
        if sound is None:
            Log.warn("SOUND NOT LOADED: note_peel")
            return
        sound.play()

    def on_release(self) -> None:
        sound = StickyNote.s_SoundBank["note_stick"]
        if sound is None:
            Log.warn("SOUND NOT LOADED: note_stick")
            return
        sound.play()


