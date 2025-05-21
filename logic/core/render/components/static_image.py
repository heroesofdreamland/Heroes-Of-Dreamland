from logic.core.render.component import Component
from logic.core.render.surface import Surface, NativeSurface
from logic.core.resource_cache import cached_image


class StaticImage(Component):
    def __init__(self, path: str, size: float | None = None):
        self.__path = path
        self.__size = size
        self.__original_image = cached_image(path=self.__path)
        super().__init__()

    def surface(self) -> Surface:
        return NativeSurface(surface=cached_image(path=self.__path, scale=self.__scale()), identifier=str(self))

    def __scale(self) -> float:
        scale: float = 1
        if self.__size is not None:
            size = self.__original_image.get_size()
            scale = self.__size / max(size[0], size[1])
        return scale

    def __hash__(self):
        return hash(self.__path)

    def __repr__(self):
        scale = self.__scale()
        size = self.__original_image.get_size()
        size = (size[0] * scale, size[1] * scale)
        return self.__class__.__name__ + "(path=" + self.__path + ", size=" + str(size) + ")"
