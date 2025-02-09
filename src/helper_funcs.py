"""Module containing helper functions"""
import pygame

def get_frame(
        sheet: pygame.Surface, frame_count: int,
        dimensions: tuple[int, int], scale: int|float
    ) -> pygame.Surface:
    """
    Function to get desired frame from a sprite sheet.
    It creates a surface then draws the frame onto it 
    and finally scaling the surface before returning it.
    """
    frame = pygame.Surface(dimensions).convert_alpha()
    frame.blit(sheet, (0, 0), ((frame_count * dimensions[0]), 0, dimensions[0], dimensions[1]))
    frame = pygame.transform.scale(frame, (dimensions[0] * scale, dimensions[1] * scale))
    frame.set_colorkey("Black")

    return frame
