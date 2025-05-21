import pygame


class Color:
    def __init__(self, r: int, g: int, b: int, a: int = 255):
        self.__r = r
        self.__g = g
        self.__b = b
        self.__a = a
        self.__pygame_color = pygame.Color(self.__r, self.__g, self.__b, self.__a)

    def __hash__(self):
        return hash((self.__r, self.__g, self.__b, self.__a))

    def __repr__(self):
        return str((self.__r, self.__g, self.__b, self.__a))

    def color(self) -> pygame.Color:
        return self.__pygame_color

    def is_clear(self) -> bool:
        return self.__a == 0
