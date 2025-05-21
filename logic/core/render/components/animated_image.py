from logic.core.animated_object import AnimatedObject
from logic.core.render.component import Component
from logic.core.render.surface import Surface, NativeSurface, EmptySurface
from logic.entities.units.models.animation_type import AnimationType


class AnimatedImage(Component):
    def __init__(self, animated_object: AnimatedObject, animation_type: AnimationType):
        self.__animated_object = animated_object
        self.__animation_type = animation_type
        super().__init__()
        self.__animated_object.configure_animation(self.__animation_type)

    def surface(self) -> Surface:
        image = self.__animated_object.get_image()
        if image is not None:
            surface, path, index = image
            identifier = self.__class__.__name__ + "(path=" + path + ", index=" + str(index) + ", scale=" + str(self.__animated_object.scale) + ", mirrored=" + str(self.__animated_object.mirrored) + ")"
            return NativeSurface(surface=surface, identifier=identifier)
        else:
            return EmptySurface()
