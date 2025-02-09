"""Module for the game loop"""
import math
import os
import sys
import pygame
from .fireball import FireBall
from .groups_and_collison import GroupsAndCollison
from .orb import Orb


class GameLoop():
    """Class which combines all game elements and starts the game."""
    def __init__(self) -> None:
        pygame.init()

        self.screen_width = 1280
        self.screen_height = 720

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Ascension")

        self.clock = pygame.time.Clock()

        self.groups = GroupsAndCollison()

        self.bg_surface = pygame.image.load("gfx/backround.png").convert_alpha()
        self.bg_width = self.bg_surface.get_width()
        self.scroll = 0
        self.tiles = math.ceil(self.screen_width / self.bg_width) + 1

        self.bg2_surface = pygame.image.load("gfx/backround2.png").convert_alpha()
        self.bg2_width = self.bg2_surface.get_width()
        self.scroll2 = 0
        self.tiles2 = math.ceil(self.screen_width / self.bg2_width) + 1

        self.bar_length = 100.0

        self.sounds = {"attack_sound": pygame.mixer.Sound("sounds/attack.mp3"),
                       "orb_break_sound": pygame.mixer.Sound("sounds/orb_break.mp3"),
                       "music": pygame.mixer.Sound("sounds/music.mp3"),
                       "transform_sound": pygame.mixer.Sound("sounds/transformation.mp3"),
                       "fireball_hit_sound": pygame.mixer.Sound("sounds/fireball_hit.mp3"),
                       "victory_sound": pygame.mixer.Sound("sounds/victory.mp3")}

        self.orb_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.orb_timer, 1000)

        self.fireball_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.fireball_timer, 1400)

        self.phases = {"first_phase_active": True,
                       "second_phase_active": False,
                       "victory": False}

        self.start_time = 0

        self.final_time = 0
        self.best_time = 0


    def display_time(self, color) -> int:
        """Function which tracks the elapsed time and displays it."""
        current_time = (pygame.time.get_ticks() - self.start_time) // 1000
        font = pygame.font.Font(None, 50)

        time_text_surf = font.render("Time", False, color)
        time_text_rect = time_text_surf.get_rect(center = (150, 80))

        time_surf = font.render(f"{current_time}", False, color)
        time_rect = time_surf.get_rect(center = (150, 120))

        self.screen.blit(time_text_surf, time_text_rect)
        self.screen.blit(time_surf, time_rect)

        return current_time

    def draw_energy_bar(self, color) -> None:
        """Function which draws the energy bar on the screen for each frame of the game."""
        font = pygame.font.Font(None, 50)
        text_surface = font.render("Energy", False, color)
        text_rect = text_surface.get_rect(center = (640, 50))
        self.screen.blit(text_surface, text_rect)

        pygame.draw.rect(self.screen, "Yellow", pygame.Rect(400, 70, self.bar_length, 70))
        pygame.draw.rect(self.screen, color, pygame.Rect(400, 70, 500, 70), 6)

    def bar_progress(self) -> None:
        """
        Function which reduces the energy bar each frame,
        checks the energy bar's state and changes game phases accordingly
        and keeps track of the best time for completion of the game using a file.
        """
        self.bar_length -= 0.25

        if self.bar_length <= 0:
            self.final_time = self.display_time("White")
            self.phases["first_phase_active"] = False
            self.phases["second_phase_active"] = False
        elif self.bar_length >= 500:
            self.bar_length = 500
            self.final_time = self.display_time("white")
            with open("best_score.txt", "a+", encoding = "utf-8") as file:

                if os.stat("best_score.txt").st_size == 0:
                    file.write(f"{self.final_time}")
                    self.best_time = self.final_time
                else:
                    file.seek(0)
                    content = file.readline()

                    if int(content) < self.final_time:
                        self.best_time = int(content)
                    else:
                        file.truncate(0)
                        file.write(f"{self.final_time}")
                        self.best_time = self.final_time

            self.phases["second_phase_active"] = False
            self.phases["victory"] = True

    def draw_victory_screen(self) -> None:
        """Function which draws the victory screen upon successful completion of the game."""
        self.screen.fill("Black")
        victory_font = pygame.font.Font(None, 150)
        victory_text_surf = victory_font.render("Congratulations!", False, "White")
        victory_text_rect = victory_text_surf.get_rect(center = (625, 300))
        self.screen.blit(victory_text_surf, victory_text_rect)

        time_font = pygame.font.Font(None, 75)
        best_text_surf = time_font.render(f"Best time: {self.best_time} seconds", False, "White")
        best_text_rect = best_text_surf.get_rect(center = (625, 415))
        fin_text_surf = time_font.render(f"Finish time: {self.final_time} seconds", False, "White")
        fin_text_rect = fin_text_surf.get_rect(center = (625, 375))
        self.screen.blit(fin_text_surf, fin_text_rect)
        self.screen.blit(best_text_surf, best_text_rect)

    def draw_game_over(self) -> None:
        """Function which draws the game over screen upon the energy bar depleting completely"""
        self.screen.fill("Black")
        game_over_font = pygame.font.Font(None, 150)
        over_text_surf = game_over_font.render("Game Over", False, "White")
        over_text_rect = over_text_surf.get_rect(center = (625, 300))
        self.screen.blit(over_text_surf, over_text_rect)

        time_font = pygame.font.Font(None, 75)
        fin_text_surf = time_font.render(f"Finish time: {self.final_time} seconds", False, "White")
        finish_text_rect = fin_text_surf.get_rect(center = (625, 375))
        self.screen.blit(fin_text_surf, finish_text_rect)

    def draw_retry_button(self) -> None:
        """Function which draws the retry button on the victory/game over screen, 
        which restarts the game upon being clicked"""
        self.sounds["music"].stop()
        pygame.draw.rect(self.screen, "White", pygame.Rect(475, 450, 300, 80), 6)

        mouse_pos = pygame.mouse.get_pos()
        if pygame.Rect(475, 450, 300, 80).collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.start_time = pygame.time.get_ticks()
                self.bar_length = 100
                self.groups.orb_group.empty()
                self.groups.fireball_group.empty()
                self.groups.char1.reset()
                self.groups.char2.reset()
                self.sounds["music"].play(loops = -1)
                self.phases["first_phase_active"] = True
                self.phases["victory"] = False

        retry_over_font = pygame.font.Font(None, 90)
        retry_text_surf = retry_over_font.render("Retry", False, "White")
        retry_text_rect = retry_text_surf.get_rect(center = (625, 490))
        self.screen.blit(retry_text_surf, retry_text_rect)

    def draw_phases(self) -> None:
        """Function which draws the screen for each phase of the game"""
        if self.phases["first_phase_active"]:
            for i in range(0, self.tiles):
                self.screen.blit(self.bg_surface, (i * self.bg_width + self.scroll, 0))

            self.scroll -= 10

            if abs(self.scroll) > self.bg_width:
                self.scroll = 0

            if self.bar_length >= 250:
                self.sounds["transform_sound"].play()
                self.groups.orb_group.empty()
                self.phases["first_phase_active"] = False
                self.phases["second_phase_active"] = True

            self.bar_progress()
            self.draw_energy_bar("Black")

            self.groups.char1_group.draw(self.screen)
            self.groups.char1_group.update()

            self.groups.orb_group.draw(self.screen)
            self.groups.orb_group.update(10)

            self.display_time("Black")
        elif self.phases["second_phase_active"]:
            for i in range(0, self.tiles2):
                self.screen.blit(self.bg2_surface, (i * self.bg2_width + self.scroll2, 0))

            self.scroll2 -= 8

            if abs(self.scroll2) > self.bg2_width:
                self.scroll2 = 0

            if self.bar_length >= 500:
                self.sounds["music"].stop()
                self.sounds["victory_sound"].play()

            self.bar_progress()
            self.draw_energy_bar("White")

            self.groups.char2_group.draw(self.screen)
            self.groups.char2_group.update()

            self.groups.orb_group.draw(self.screen)
            self.groups.orb_group.update(20)

            self.groups.fireball_group.draw(self.screen)
            self.groups.fireball_group.update()

            if self.groups.collision_char2_orb():
                self.sounds["orb_break_sound"].play()
                self.bar_length += 30

            if self.groups.collision_char2_fireball():
                self.bar_length -= 20
                self.sounds["fireball_hit_sound"].play()

            self.display_time("White")
        elif self.phases["victory"]:
            self.draw_victory_screen()
            self.draw_retry_button()
        else:
            self.draw_game_over()
            self.draw_retry_button()

    def run(self) -> None:
        """Function which starts the game loop and checks for events"""
        self.sounds["music"].play(loops = -1)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.phases["first_phase_active"]:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.sounds["attack_sound"].play()
                        if self.groups.collision_char1_orb():
                            self.sounds["orb_break_sound"].play()
                            self.bar_length += 30
                    if event.type == self.orb_timer:
                        self.groups.orb_group.add(Orb((1300, 1500), (250, 475)))
                if self.phases["second_phase_active"]:
                    if event.type == self.orb_timer:
                        self.groups.orb_group.add(Orb((1500, 1700), (200, 600)))
                    if event.type == self.fireball_timer:
                        self.groups.fireball_group.add(FireBall())

            self.draw_phases()

            pygame.display.update()
            self.clock.tick(60)
