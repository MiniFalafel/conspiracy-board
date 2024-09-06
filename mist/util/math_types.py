
from mist.util.log import Log

class Vector:
    def __init__(self, *args):
        self.elements = [*args]

    # 'VIRTUAL' overridable method for subclasses to implement
    def get_el_count(self) -> int:
        return 0

class vec2 (Vector):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y)

    def get_el_count(self) -> int:
        return 2

    # OPERATOR OVERLOADS
    def __add__(self, other: Vector):
        # Check if the element counts are the same
        if self.get_el_count() == other.get_el_count():
            return vec2(*[self.elements[i] + other.elements[i] for i in range(self.get_el_count())])

        else:
            Log.warn("Vectors are NOT of equal size! Returning original vector")
            return self

    def __sub__(self, other: Vector):
        # Check if the element counts are the same
        if self.get_el_count() == other.get_el_count():
            return vec2(*[self.elements[i] - other.elements[i] for i in range(self.get_el_count())])

        else:
            Log.warn("Vectors are NOT of equal size! Returning original vector")
            return self

    def __mul__(self, other: Vector):
        # Check if the element counts are the same
        if self.get_el_count() == other.get_el_count():
            return vec2(*[self.elements[i] * other.elements[i] for i in range(self.get_el_count())])

        else:
            Log.warn("Vectors are NOT of equal size! Returning original vector")
            return self

    def __truediv__(self, other: Vector):
        # Check if the element counts are the same
        if self.get_el_count() == other.get_el_count():
            return vec2(*[self.elements[i] / other.elements[i] for i in range(self.get_el_count())])

        else:
            Log.warn("Vectors are NOT of equal size! Returning original vector")
            return self

    # GET ITEM
    def __getitem__(self, item: int):
        return self.elements[item]

    # COPY
    def copy(self):
        return vec2(*self.elements[:])


