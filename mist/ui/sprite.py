import pygame.sprite
from mist.util.math_types import vec2

class SpriteLoader:

    __s_SpriteData = {}

    @staticmethod
    def load(path: str, scale: tuple[int, int] = None):
        # Create a key for the data hashmap
        key = path + str(scale)

        # Make sure data doesn't already exist
        if not key in SpriteLoader.__s_SpriteData.keys():
            img = pygame.image.load(path)
            # resize (if relevant)
            if scale is not None:
                img = pygame.transform.scale(img, scale)
            # Update the dictionary
            SpriteLoader.__s_SpriteData[key] = img
        # Return whatever is at the key now
        return SpriteLoader.__s_SpriteData[key]

        # If not, load and add to the hashmap

class Sprite(pygame.sprite.Sprite):
    def __init__(self, path: str, scale: vec2 = None):
        super().__init__()

        # use the sprite loader to load the asset
        self.image = SpriteLoader.load(path, scale.elements)
        self.rect = pygame.rect.Rect(0, 0, scale[0], scale[1])

    def draw(self, surface, offset: vec2):
        surface.blit(self.image, offset.elements)


