"""Module for player character in the first phase of the game"""
import pygame
from .helper_funcs import get_frame

class CharacterOne(pygame.sprite.Sprite):
    """Class which represents the player character in the first phase."""


    def __init__(self) -> None:
        super().__init__()

        self.sheets = {
            "run_sheet": pygame.image.load("gfx/char_phase_one/Run.png").convert_alpha(),
            "jump_sheet": pygame.image.load("gfx/char_phase_one/Jump.png").convert_alpha(),
            "attack_sheet": pygame.image.load("gfx/char_phase_one/Attack.png").convert_alpha()
        }

        self.frames = {
            "run_frames": 
                [get_frame(self.sheets["run_sheet"], i, (42, 42), 4) for i in range(6)],
            "jump_frames": 
                [get_frame(self.sheets["jump_sheet"], i, (42, 42), 4) for i in range(8)],
            "attack_frames": 
                [get_frame(self.sheets["attack_sheet"], i, (42, 42), 4) for i in range(6)]
        }

        self.indexes = {
            "frame_index": 0.0,
            "attack_frame_index": 0.0,
            "left_clicked": False
        }
        self.coords_change = [0.0, 0.0]

        self.start_coords = (90, 605)

        self.image = self.frames["run_frames"][int(self.indexes["frame_index"])]
        self.rect = self.image.get_rect(midbottom = (self.start_coords[0], self.start_coords[1]))

    def input(self) -> None:
        """Function which tracks player input"""
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 605:
            self.coords_change[1] = -25

        if keys[pygame.K_d]:
            self.coords_change[0] += 0.25

        if keys[pygame.K_a]:
            self.coords_change[0] -= 0.25

        if not any(keys):
            self.coords_change[0] = 0

        if mouse[0]:
            self.indexes["left_clicked"] = True


    def apply_movement(self) -> None:
        """
        Function which moves the player character depending on what is pressed
        and sets boundaries on the screen so the player character cannot leave it.
        """
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 1280:
            self.rect.right = 1280

        self.coords_change[1] += 1
        self.rect.y += int(self.coords_change[1])

        self.rect.bottom = min(self.rect.bottom, 605)

        self.rect.x += int(self.coords_change[0])

    def animation(self) -> None:
        """Function which animates the character sprite depending on player input."""
        if self.indexes["left_clicked"]:
            self.indexes["attack_frame_index"] += 0.2
            if self.indexes["attack_frame_index"] >= len(self.frames["attack_frames"]):
                self.indexes["attack_frame_index"] = 0
                self.indexes["left_clicked"] = False
            self.image = self.frames["attack_frames"][int(self.indexes["attack_frame_index"])]
        elif self.rect.bottom < 605:
            self.indexes["frame_index"] += 0.1
            if self.indexes["frame_index"] >= len(self.frames["jump_frames"]):
                self.indexes["frame_index"] = 0
            self.image = self.frames["jump_frames"][int(self.indexes["frame_index"])]
        else:
            self.indexes["frame_index"] += 0.3
            if self.indexes["frame_index"] >= len(self.frames["run_frames"]):
                self.indexes["frame_index"] = 0
            self.image = self.frames["run_frames"][int(self.indexes["frame_index"])]

    def reset(self) -> None:
        """Function which returns player character at the starting position upon restart."""
        self.rect.midbottom = (self.start_coords[0], self.start_coords[1])

    def update(self) -> None:
        """Function to update the player character for each frame of the game."""
        self.input()
        self.apply_movement()
        self.animation()
