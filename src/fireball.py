"""Module for firaball obstacle in the second phase"""
from random import randint
import pygame
from .helper_funcs import get_frame

class FireBall(pygame.sprite.Sprite):
    """Class which represents the fireballs in the second phase of the game."""


    def __init__(self) -> None:
        super().__init__()

        self.sheet = pygame.image.load("gfx/fireball.png").convert_alpha()
        self.frames = [get_frame(self.sheet, i, (63, 43), 4) for i in range(8)]

        self.frame_index = 0.0

        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(topleft = (randint(1500, 1700), randint(250, 600)))

    def disappear(self) -> None:
        """Functions which removes a fireball once it leaves the screen."""
        if self.rect.x <= -100:
            self.kill()

    def animation(self) -> None:
        """Function which animates the fireball by going trough the list of frames."""
        self.frame_index += 0.05
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self) -> None:
        """Function which updates the fireball for each frame of the game."""
        self.rect.x -= 25
        self.animation()
        self.disappear()
