import pygame


class BackgroundSound:
    def __init__(self, sound_path: str, volume: float, is_repeated: int|None = None):
        self.sound_path = sound_path
        self.volume = volume
        self.is_repeated = is_repeated

    def play(self):
        pygame.mixer.music.play(self.is_repeated)

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def change_volume(self, volume: float):
        pygame.mixer.music.set_volume(volume)



