import math
import pygame
import game_functions as gf
from pygame.sprite import Sprite
from image_rect import ImageRect


class PMAN(Sprite):
    PAC_MAN_SIZE = 30

    def __init__(self, screen, maze):
        super(PMAN, self).__init__()
        self.screen = screen.get_rect()
        self.image = ImageRect(screen, "pac_left_2", PMAN.PAC_MAN_SIZE, PMAN.PAC_MAN_SIZE)
        self.rect = self.image.rect
        self.rect.x = self.screen.centerx - 10
        self.rect.y = self.screen.centery + 110

        self.maze = maze
        self.direction = "l"
        self.move = "l"
        self.speed = 5
        self.tick_speed = 10
        self.timer = pygame.time.get_ticks()

        # images
        self.index = 1
        self.dead_index = 1
        self.sound_index = 1

        self.direction_l = False
        self.direction_r = False
        self.direction_u = False
        self.direction_d = False
        self.lives = 3
        self.score = 0

    def update(self, maze, screen):
        if gf.ball_stop(self, maze) is False and pygame.time.get_ticks() - self.timer >= self.tick_speed:
            self.timer = pygame.time.get_ticks()
            if self.move == "l":
                self.image.rect.x -= self.speed
                file = "pac_left_" + str(math.floor(self.index))
            elif self.move == "r":
                self.image.rect.x += self.speed
                file = "pac_right_" + str(math.floor(self.index))
            elif self.move == "d":
                self.image.rect.y += self.speed
                file = "pac_down_" + str(math.floor(self.index))
            elif self.move == "u":
                self.image.rect.y -= self.speed
                file = "pac_up_" + str(math.floor(self.index))
            else:
                file = "p_up_1"
            self.image = ImageRect(screen, file, PMAN.PAC_MAN_SIZE, PMAN.PAC_MAN_SIZE)
            self.image.rect = self.rect
            if self.index >= 4:
                self.index = 1
            else:
                self.index += .3

    def ghost_collision(self, redghost, blueghost, pinkghost, orangeghost, stats, screen):
        if pygame.sprite.collide_rect(self, redghost) and redghost.alive is True:
            stats.game_pause = True
            die = pygame.mixer.Sound('sounds/death.wav')
            die.play()
        elif pygame.sprite.collide_rect(self, blueghost) and blueghost.alive is True:
            stats.game_pause = True
            die = pygame.mixer.Sound('sounds/death.wav')
            die.play()
        elif pygame.sprite.collide_rect(self, pinkghost) and pinkghost.alive is True:
            stats.game_pause = True
            die = pygame.mixer.Sound('sounds/death.wav')
            die.play()
        elif pygame.sprite.collide_rect(self, orangeghost) and orangeghost.alive is True:
            stats.game_pause = True
            die = pygame.mixer.Sound('sounds/death.wav')
            die.play()

        if stats.game_pause and redghost.alive is True:
            file = "pac_dead_" + str(math.floor(self.dead_index))
            self.image = ImageRect(screen, file, PMAN.PAC_MAN_SIZE, PMAN.PAC_MAN_SIZE)
            self.image.rect = self.rect
            if self.dead_index >= 6:
                self.dead_index = 1
                stats.game_pause = False
                self.lives -= 1
                gf.reset(self, redghost, blueghost, pinkghost, orangeghost, stats)
            else:
                self.dead_index += .2

        if self.lives == 0:
            stats.game_over = True

    def blitme(self):
        self.image.blitme()
