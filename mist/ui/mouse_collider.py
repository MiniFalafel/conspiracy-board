from mist.util.math_types import vec2

class MouseCollider:
    def __init__(self, pos: vec2):
        self.pos = pos

    # "VIRTUAL" methods -----------------------------
    # Check collision
    def check_collision(self, mouse_pos: vec2) -> bool:
        pass

    # Getter
    def get_pos(self) -> vec2:
        return self.pos.copy()

    # Setter
    def set_pos(self, pos: vec2) -> None:
        self.pos = pos

class MouseBoxCollider (MouseCollider):
    def __init__(self, pos: vec2, dimensions: vec2):
        super().__init__(pos)
        self.dim = dimensions

    # GETTERS
    def get_dim(self) -> vec2:
        return self.dim.copy()

    # SETTERS
    def set_dim(self, dimensions: vec2) -> None:
        self.dim = dimensions

    # VIRTUAL OVERRIDES
    def check_collision(self, mouse_pos: vec2) -> bool:
        offset = mouse_pos - self.pos
        for axis in range(2):
            if offset[axis] < 0:
                return False
            if offset[axis] > self.dim[axis]:
                return False
        return True

