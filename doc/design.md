# Mist Design

This is a design document where I'll write down plans for features


## Text Input UI Element
1. Rendering:
    * All text should render onto its own surface whose height is independent of the container size
    * Then, the container will draw onto a surface of the same size as the container.
    * Text surface will be 'blit'ed onto the container surface with a Y offset based on scroll amount
2. Behavior:
    * When the user clicks on the element, it should come into **focus**
        * Visual indicator?
    * When focused, a cursor will indicate where the user is typing
    * Text should wrap around _(maybe there could be an option to disable this?)_
    * Return and Enter will both be interpreted as newlines _(for the sake of my sanity)_
    * When the user clicks anywhere other than the text input, it should **un-focus**
3. User Input:
    * Obviously, typing should add text to the box.
    * Mouse scroll while the mouse is hovering should scroll through the text
    * Clicking on the element **focuses**
    * Clicking off the element **un-focuses**
    * Resizable?

TODO: Add documentation for existing features. Will do later bc I'm going to a bbq! (epic swag)

