"""Main"""
import sys
from random import randint
import math
import os
import pygame


class CharacterOne(pygame.sprite.Sprite):
    """Class which represents the player character in the first phase."""


    def __init__(self) -> None:
        super().__init__()

        self.sheets = {
            "run_sheet": pygame.image.load("gfx/char_phase_one/run.png").convert_alpha(),
            "jump_sheet": pygame.image.load("gfx/char_phase_one/jump.png").convert_alpha(),
            "attack_sheet": pygame.image.load("gfx/char_phase_one/attack.png").convert_alpha()
        }

        self.frames = {
            "run_frames": 
                [self.__get_frame(self.sheets["run_sheet"], i, (42, 42), 4) for i in range(6)],
            "jump_frames": 
                [self.__get_frame(self.sheets["jump_sheet"], i, (42, 42), 4) for i in range(8)],
            "attack_frames": 
                [self.__get_frame(self.sheets["attack_sheet"], i, (42, 42), 4) for i in range(6)]
        }

        self.frame_index = 0.0
        self.attack_frame_index = 0.0

        self.coords_change = [0.0, 0.0]

        self.clicked = False

        self.start_coords = (90, 605)

        self.image = self.frames["run_frames"][int(self.frame_index)]
        self.rect = self.image.get_rect(midbottom = (self.start_coords[0], self.start_coords[1]))


    def __get_frame(
            self, sheet: pygame.Surface, frame_count: int,
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
            self.clicked = True


    def apply_gravity(self) -> None:
        """Function which moves the player character depending on what is pressed."""
        self.coords_change[1] += 1
        self.rect.y += int(self.coords_change[1])

        self.rect.bottom = min(self.rect.bottom, 605)

        self.rect.x += int(self.coords_change[0])

    def animation(self) -> None:
        """Function which animates the character sprite depending on player input."""
        if self.clicked:
            self.attack_frame_index += 0.2
            if self.attack_frame_index >= len(self.frames["attack_frames"]):
                self.attack_frame_index = 0
                self.clicked = False
            self.image = self.frames["attack_frames"][int(self.attack_frame_index)]
        elif self.rect.bottom < 605:
            self.frame_index += 0.1
            if self.frame_index >= len(self.frames["jump_frames"]):
                self.frame_index = 0
            self.image = self.frames["jump_frames"][int(self.frame_index)]
        else:
            self.frame_index += 0.3
            if self.frame_index >= len(self.frames["run_frames"]):
                self.frame_index = 0
            self.image = self.frames["run_frames"][int(self.frame_index)]

    def reset(self) -> None:
        """Function which returns player character at the starting position upon restart."""
        self.rect.midbottom = (self.start_coords[0], self.start_coords[1])

    def update(self) -> None:
        """Function to update the player character for each frame of the game."""
        self.input()
        self.apply_gravity()
        self.animation()

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

class FireBall(pygame.sprite.Sprite):
    """Class which represents the fireballs in the second phase of the game."""


    def __init__(self) -> None:
        super().__init__()

        self.sheet = pygame.image.load("gfx/fireball.png").convert_alpha()
        self.frames = [self.__get_frame(self.sheet, i, (63, 43), 4) for i in range(8)]

        self.frame_index = 0.0

        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(topleft = (randint(1500, 1700), randint(250, 600)))

    def __get_frame(
            self, sheet: pygame.Surface, frame_count: int,
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
                [self.__get_frame(self.sheets["fly_n_sheet"], i, (52, 28), 3.5) for i in range(3)],
            "fly_up_frames": 
                [self.__get_frame(self.sheets["fly_up_sheet"], i, (48, 28), 3.5) for i in range(4)],
            "fly_down_frames": 
               [self.__get_frame(self.sheets["fly_down_sheet"], i, (51, 28), 3.5) for i in range(4)]
        }

        self.frame_index = 0.0

        self.coords_change = [0.0, 0.0]

        self.start_coords = (120, 400)

        self.image = self.frames["fly_n_frames"][int(self.frame_index)]
        self.rect = self.image.get_rect(midbottom = (self.start_coords[0], self.start_coords[1]))

    def __get_frame(
            self, sheet: pygame.Surface, frame_count: int,
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
                       "bg_music": pygame.mixer.Sound("sounds/music_phase_1.mp3"),
                       "bg_music2": pygame.mixer.Sound("sounds/music_phase_2.mp3"),
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
        self.sounds["bg_music2"].stop()
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
                self.sounds["bg_music2"].play(loops = -1)
                self.phases["first_phase_active"] = True

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

            self.scroll2 -= 5

            if abs(self.scroll2) > self.bg2_width:
                self.scroll2 = 0

            if self.bar_length >= 500:
                self.sounds["bg_music2"].stop()
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
        self.sounds["bg_music2"].play(loops = -1)

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

game = GameLoop()
game.run()
