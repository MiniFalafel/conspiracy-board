# LAYER CLASS
class Layer:
    def __init__(self, name):
        self.name = name

    # "VIRTUAL" methods to be implemented by subclasses (not necessary in python, but is good practice for readability)
    def on_attach(self):
        pass

    def on_detach(self):
        pass

    def on_update(self):
        pass

    def on_render(self, surface):
        pass

    def on_event(self, event) -> bool:
        pass

# LAYER STACK
class LayerStack:
    def __init__(self):
        self.layers = []

    def push_layer(self, layer):
        layer.on_attach()
        self.layers.append(layer)

    def pop_layer(self) -> Layer:
        return self.layers.pop()

    def update(self):
        for layer in self.layers:
            layer.on_update()

    def render(self, surface):
        for layer in self.layers:
            layer.on_render(surface)

    def on_event(self, event) -> bool:
        for layer in self.layers:
            # if handled, return true
            if layer.on_event(event):
                return True
        # None of the layers handled the event, so return false
        return False
