"""Module for the orb object"""
from random import randint
import pygame

class Orb(pygame.sprite.Sprite):
    """Class which represents the orbs in both phases."""


    def __init__(self, rand_x_coord: tuple[int, int], rand_y_coord: tuple[int, int]) -> None:
        super().__init__()

        self.image = pygame.image.load("gfx/orb.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = (randint(*rand_x_coord), randint(*rand_y_coord)))

    def disappear(self) -> None:
        """Functions which removes an orb once it leaves the screen."""
        if self.rect.x <= -100:
            self.kill()

    def update(self, speed: int) -> None:
        """Function which updates the orb location for each frame of the game."""
        self.rect.x -= speed
        self.disappear()
