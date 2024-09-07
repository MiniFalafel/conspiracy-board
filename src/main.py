from mist import *

from my_layer import UIObjectsLayer

class MyApp(Application):
    def __init__(self):
        # Init super
        super().__init__(1280, 720, "Mystery Board POC")

        # Attach Layers
        self.layer_stack.push_layer(UIObjectsLayer())

def main():
    app = MyApp()
    app.run()


if __name__ == "__main__":
    main()
