import pygame


class Sound:
    def __init__(self, sound_path: str, volume: float, is_repeated: bool):
        self.sound_path = sound_path
        self.volume = volume
        self.is_repeated = is_repeated
        self.sound = pygame.mixer.Sound(self.sound_path)

    def play(self):
        self.sound.set_volume(self.volume)
        self.sound.play()



