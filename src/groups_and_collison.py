"""Module for sprite groups and collisons"""
import pygame
from .character_one import CharacterOne
from .character_two import CharacterTwo

class GroupsAndCollison():
    """Class for sprite groups and collisions between them."""
    def __init__(self) -> None:
        self.char1 = CharacterOne()
        self.char1_group: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
        self.char1_group.add(self.char1)

        self.char2 = CharacterTwo()
        self.char2_group: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
        self.char2_group.add(self.char2)

        self.orb_group: pygame.sprite.Group = pygame.sprite.Group()

        self.fireball_group: pygame.sprite.Group = pygame.sprite.Group()

    def collision_char1_orb(self) -> list[pygame.sprite.Sprite]:
        """
        Function to check for collisions between player character and orbs in the first phase.
        """
        return pygame.sprite.spritecollide(self.char1_group.sprite, self.orb_group, True)

    def collision_char2_orb(self) -> list[pygame.sprite.Sprite]:
        """
        Function to check for collisions between player character and orbs in the second phase.
        """
        return pygame.sprite.spritecollide(self.char2_group.sprite, self.orb_group, True)

    def collision_char2_fireball(self) -> list[pygame.sprite.Sprite]:
        """
        Function to check for collisions between player character and fireballs in the second phase.
        """
        return pygame.sprite.spritecollide(self.char2_group.sprite, self.fireball_group, True)
