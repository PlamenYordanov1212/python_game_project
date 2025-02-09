"""Module for player character in the second phase of the game"""
import pygame
from .helper_funcs import get_frame

class CharacterTwo(pygame.sprite.Sprite):
    """Class which represents the player character in the second phase."""


    def __init__(self) -> None:
        super().__init__()

        self.sheets = {
            "fly_n_sheet": pygame.image.load("gfx/char_phase_two/fly_n.png").convert_alpha(),
            "fly_up_sheet": pygame.image.load("gfx/char_phase_two/fly_up.png").convert_alpha(),
            "fly_down_sheet": pygame.image.load("gfx/char_phase_two/fly_down.png").convert_alpha()
        }

        self.frames = {
            "fly_n_frames": 
                [get_frame(self.sheets["fly_n_sheet"], i, (52, 28), 3.5) for i in range(3)],
            "fly_up_frames": 
                [get_frame(self.sheets["fly_up_sheet"], i, (48, 28), 3.5) for i in range(4)],
            "fly_down_frames": 
                [get_frame(self.sheets["fly_down_sheet"], i, (51, 28), 3.5) for i in range(4)]
        }

        self.frame_index = 0.0

        self.coords_change = [0.0, 0.0]

        self.start_coords = (120, 400)

        self.image = self.frames["fly_n_frames"][int(self.frame_index)]
        self.rect = self.image.get_rect(midbottom = (self.start_coords[0], self.start_coords[1]))

    def input(self) -> None:
        """Function which tracks player input."""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.coords_change[1] -= 0.30

        if keys[pygame.K_s]:
            self.coords_change[1] += 0.30

        if keys[pygame.K_d]:
            self.coords_change[0] += 0.30

        if keys[pygame.K_a]:
            self.coords_change[0] -= 0.30

        if not any(keys):
            self.coords_change[0] = 0
            self.coords_change[1] = 0

    def apply_movement(self) -> None:
        """
        Function which moves the player character depending on what was pressed
        and sets boundaries on the screen so the player character cannot leave it.
        """
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 1280:
            self.rect.right = 1280
        elif self.rect.bottom > 720:
            self.rect.bottom = 720
        elif self.rect.top < 0:
            self.rect.top = 0


        self.rect.x += int(self.coords_change[0])
        self.rect.y += int(self.coords_change[1])

    def animation(self) -> None:
        """
        Function which animates the character sprite depending on player input 
        by going trough the respective list of frames.
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.frame_index += 0.2
            if self.frame_index >= len(self.frames["fly_up_frames"]):
                self.frame_index = 0
            self.image = self.frames["fly_up_frames"][int(self.frame_index)]
        elif keys[pygame.K_s]:
            self.frame_index += 0.1
            if self.frame_index >= len(self.frames["fly_down_frames"]):
                self.frame_index = 0
            self.image = self.frames["fly_down_frames"][int(self.frame_index)]
        else:
            self.frame_index += 0.1
            if self.frame_index >= len(self.frames["fly_n_frames"]):
                self.frame_index = 0
            self.image = self.frames["fly_n_frames"][int(self.frame_index)]

    def reset(self) -> None:
        """Function which returns player character at the starting position upon restart."""
        self.rect.midbottom = (self.start_coords[0], self.start_coords[1])

    def update(self) -> None:
        """Function to update the player character for each frame of the game."""
        self.input()
        self.apply_movement()
        self.animation()
