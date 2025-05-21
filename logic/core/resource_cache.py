import pygame

__images_cache: dict[str, dict[tuple[bool, float], pygame.Surface]] = {}
__fonts_cache: dict[str, dict[int, pygame.font.Font]] = {}


def cached_image(path: str, mirrored: bool = False, scale: float = 1) -> pygame.Surface:
    if path not in __images_cache:
        __images_cache[path] = {}
    image_cache = __images_cache[path]
    key = mirrored, scale
    if key in image_cache:
        return image_cache[key]

    original_image_key = (False, 1)
    original_image: pygame.Surface
    if original_image_key in __images_cache[path]:
        original_image = __images_cache[path][original_image_key]
    else:
        original_image = pygame.image.load(path)
        __images_cache[path][key] = original_image

    image = original_image
    if scale != 1:
        image = pygame.transform.scale(image, (original_image.get_width() * scale, original_image.get_height() * scale))
    if mirrored:
        image = pygame.transform.flip(image, True, False)
    __images_cache[path][key] = image

    return image


def cached_font(path: str, size: int) -> pygame.font.Font:
    if path not in __fonts_cache:
        __fonts_cache[path] = {}
    font_cache = __fonts_cache[path]
    if size in font_cache:
        return font_cache[size]
    font = pygame.font.Font(path, size)
    __fonts_cache[path][size] = font
    return font