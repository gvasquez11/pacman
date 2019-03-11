import pygame
import math
import random
import game_functions as gf
from pygame.sprite import Sprite
from image_rect import ImageRect


class RedGhost(Sprite):

    def __init__(self, screen, maze):
        super(RedGhost, self).__init__()
        self.screen = screen.get_rect()
        self.image = ImageRect(screen, "red_left_1", 30, 30)
        self.rect = self.image.rect
        self.rect.x = 300
        self.rect.y = 230
        self.maze = maze
        self.direction = "u"
        self.move = "u"
        self.speed = 5
        self.tick_dead = 30
        self.tick_alive = 10
        self.tick_speed = self.tick_alive
        self.index = 1
        self.dead_index = 1
        self.dead_timer = 1
        self.directions_remain = []
        self.alive = True
        self.eat = False
        self.timer = pygame.time.get_ticks()

    def update(self, maze, screen, pm):
        if gf.ball_stop(self, maze) is False and pygame.time.get_ticks() - self.timer >= self.tick_speed:
            self.timer = pygame.time.get_ticks()
            if self.move == "l":
                self.image.rect.x -= self.speed
                if self.eat is False:
                    file = "red_left_" + str(math.floor(self.index))
                else:
                    file = "eyes_left"
            elif self.move == "r":
                self.image.rect.x += self.speed
                if self.eat is False:
                    file = "red_right_" + str(math.floor(self.index))
                else:
                    file = "eyes_right"
            elif self.move == "d":
                self.image.rect.y += self.speed
                if self.eat is False:
                    file = "red_down_" + str(math.floor(self.index))
                else:
                    file = "eyes_down"
            elif self.move == "u":
                self.image.rect.y -= self.speed
                if self.eat is False:
                    file = "red_up_" + str(math.floor(self.index))
                else:
                    file = "eyes_up"
            else:
                file = "red_left_1"
            self.image = ImageRect(screen, file, 30, 30)
            self.image.rect = self.rect
            if self.index > 2.5:
                self.index = 1
            else:
                self.index += .1

        if self.alive is False and self.eat is False:
            file = "blink_" + str(math.floor(self.dead_index))
            self.image = ImageRect(screen, file, 30, 30)
            self.image.rect = self.rect
            if self.dead_timer > 20:
                self.alive = True
            else:
                self.dead_timer += .05
                if self.dead_timer < 15:
                    if self.dead_index > 2.5:
                        self.dead_index = 1
                    else:
                        self.dead_index += .1
                else:
                    if self.dead_index > 3.5:
                        self.dead_index = 2
                    else:
                        self.dead_index += .1

        if self.alive is True:
            self.tick_speed = self.tick_alive
        elif self.alive is False:
            self.tick_speed = self.tick_dead

        self.self_movement(maze)
        self.dead_collide(pm, maze)

    def self_movement(self, maze):
        if self.move == "u" and self.rect == (300, 230, 30, 30):
            self.move = "l"

        elif 295 < self.rect.x < 305 and 325 < self.rect.y < 335:
            self.move = "u"

        if gf.ball_stop(self, maze) is True and self.eat is False:
            self.check_directions(maze)
            if len(self.directions_remain) == 0:
                self.move = "l"
                self.move = "r"
                self.move = "u"
                self.move = "d"
            else:
                rand = random.choice(self.directions_remain)
                self.move = rand

        if self.eat is True:
            self.check_directions(maze)

            if self.rect.x < 190 and self.rect.y is not 230:
                if "r" in self.directions_remain:
                    self.move = "r"
                elif gf.ball_stop(self, maze):
                    rand = random.choice(self.directions_remain)
                    self.move = rand

            elif self.rect.x > 410 and self.rect.y is not 230:
                if "l" in self.directions_remain:
                    self.move = "l"
                elif gf.ball_stop(self, maze):
                    rand = random.choice(self.directions_remain)
                    self.move = rand

            elif self.rect.y < 230 and self.rect.x is not 300:
                if "d" in self.directions_remain:
                    self.move = "d"
                elif gf.ball_stop(self, maze):
                    rand = random.choice(self.directions_remain)
                    self.move = rand

            elif self.rect.y > 230 and self.rect.x is not 300:
                if "u" in self.directions_remain:
                    self.move = "u"
                elif gf.ball_stop(self, maze):
                    rand = random.choice(self.directions_remain)
                    self.move = rand

            elif self.rect.y is 230 and 190 < self.rect.x < 410:
                if 295 < self.rect.x < 305:
                    self.move = "d"
                elif self.rect.x < 300:
                    self.move = "r"
                elif self.rect.x > 300:
                    self.move = "l"
            else:
                rand = random.choice(self.directions_remain)
                self.move = rand

    def check_directions(self, maze):
        self.directions_remain.clear()
        self.direction = "u"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "d":
                self.directions_remain.append("u")

        self.direction = "d"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "u":
                self.directions_remain.append("d")

        self.direction = "l"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "r":
                self.directions_remain.append("l")

        self.direction = "r"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "l":
                self.directions_remain.append("r")

    def blitme(self):
        self.image.blitme()

    def dead_collide(self, pm, maze):
        if pygame.sprite.collide_rect(self, pm) and self.alive is False:
            if self.alive is False and self.eat is False:
                pm.score += 200
                eat = pygame.mixer.Sound('sounds/eatghost.wav')
                eat.play()
                self.eat = True

        if self.eat is True:
            for lines in maze.lines:
                if lines.colliderect(self):
                    self.eat = False
                    self.alive = True


class BlueGhost(Sprite):

    def __init__(self, screen, maze):
        super(BlueGhost, self).__init__()
        self.screen = screen.get_rect()
        self.image = ImageRect(screen, "blue_left_1", 30, 30)
        self.rect = self.image.rect
        self.rect.x = 250
        self.rect.y = 330
        self.maze = maze
        self.direction = "u"
        self.move = "u"
        self.speed = 5
        self.tick_dead = 30
        self.tick_alive = 10
        self.tick_speed = self.tick_alive
        self.index = 1
        self.dead_index = 1
        self.dead_timer = 1
        self.directions_remain = []
        self.alive = True
        self.eat = False
        self.timer = pygame.time.get_ticks()

    def update(self, maze, screen, pm):
        if gf.ball_stop(self, maze) is False and pygame.time.get_ticks() - self.timer >= self.tick_speed:
            self.timer = pygame.time.get_ticks()
            if self.move == "l":
                self.image.rect.x -= self.speed
                if self.eat is False:
                    file = "blue_left_" + str(math.floor(self.index))
                else:
                    file = "eyes_left"
            elif self.move == "r":
                self.image.rect.x += self.speed
                if self.eat is False:
                    file = "blue_right_" + str(math.floor(self.index))
                else:
                    file = "eyes_right"
            elif self.move == "d":
                self.image.rect.y += self.speed
                if self.eat is False:
                    file = "blue_down_" + str(math.floor(self.index))
                else:
                    file = "eyes_down"
            elif self.move == "u":
                self.image.rect.y -= self.speed
                if self.eat is False:
                    file = "blue_up_" + str(math.floor(self.index))
                else:
                    file = "eyes_up"
            else:
                file = "blue_left_1"
            self.image = ImageRect(screen, file, 30, 30)
            self.image.rect = self.rect
            if self.index > 2.5:
                self.index = 1
            else:
                self.index += .1

        if self.alive is False and self.eat is False:
            file = "blink_" + str(math.floor(self.dead_index))
            self.image = ImageRect(screen, file, 30, 30)
            self.image.rect = self.rect
            if self.dead_timer > 20:
                self.alive = True
            else:
                self.dead_timer += .05
                if self.dead_timer < 15:
                    if self.dead_index > 2.5:
                        self.dead_index = 1
                    else:
                        self.dead_index += .1
                else:
                    if self.dead_index > 3.5:
                        self.dead_index = 2
                    else:
                        self.dead_index += .1

        if self.alive is True:
            self.tick_speed = self.tick_alive
        elif self.alive is False:
            self.tick_speed = self.tick_dead

        self.self_movement(maze)
        self.dead_collide(pm, maze)

    def self_movement(self, maze):
        if self.move == "u" and self.rect == (300, 230, 30, 30):
            self.move = "l"

        elif 295 < self.rect.x < 305 and 325 < self.rect.y < 335:
            self.move = "u"

        if gf.ball_stop(self, maze) is True and self.eat is False:
            self.check_directions(maze)
            if len(self.directions_remain) == 0:
                self.move = "l"
                self.move = "r"
                self.move = "u"
                self.move = "d"
            else:
                rand = random.choice(self.directions_remain)
                self.move = rand

        if self.eat is True:
            self.check_directions(maze)

            if self.rect.x < 190 and self.rect.y is not 230:
                if "r" in self.directions_remain:
                    self.move = "r"
                elif gf.ball_stop(self, maze):
                    rand = random.choice(self.directions_remain)
                    self.move = rand

            elif self.rect.x > 410 and self.rect.y is not 230:
                if "l" in self.directions_remain:
                    self.move = "l"
                elif gf.ball_stop(self, maze):
                    rand = random.choice(self.directions_remain)
                    self.move = rand

            elif self.rect.y < 230 and self.rect.x is not 300:
                if "d" in self.directions_remain:
                    self.move = "d"
                elif gf.ball_stop(self, maze):
                    rand = random.choice(self.directions_remain)
                    self.move = rand

            elif self.rect.y > 230 and self.rect.x is not 300:
                if "u" in self.directions_remain:
                    self.move = "u"
                elif gf.ball_stop(self, maze):
                    rand = random.choice(self.directions_remain)
                    self.move = rand

            elif self.rect.y is 230 and 190 < self.rect.x < 410:
                if 295 < self.rect.x < 305:
                    self.move = "d"
                elif self.rect.x < 300:
                    self.move = "r"
                elif self.rect.x > 300:
                    self.move = "l"
            else:
                rand = random.choice(self.directions_remain)
                self.move = rand

    def check_directions(self, maze):
        self.directions_remain.clear()
        self.direction = "u"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "d":
                self.directions_remain.append("u")

        self.direction = "d"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "u":
                self.directions_remain.append("d")

        self.direction = "l"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "r":
                self.directions_remain.append("l")

        self.direction = "r"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "l":
                self.directions_remain.append("r")

    def blitme(self):
        self.image.blitme()

    def dead_collide(self, pm, maze):
        if pygame.sprite.collide_rect(self, pm) and self.alive is False:
            if self.alive is False and self.eat is False:
                pm.score += 200
                eat = pygame.mixer.Sound('sounds/eatghost.wav')
                eat.play()
                self.eat = True

        if self.eat is True:
            for lines in maze.lines:
                if lines.colliderect(self):
                    self.eat = False
                    self.alive = True


class PinkGhost(Sprite):

    def __init__(self, screen, maze):
        super(PinkGhost, self).__init__()
        self.screen = screen.get_rect()
        self.image = ImageRect(screen, "pink_left_1", 30, 30)
        self.rect = self.image.rect
        self.rect.x = 300
        self.rect.y = 330
        self.maze = maze
        self.direction = "u"
        self.move = "u"
        self.speed = 5
        self.tick_dead = 30
        self.tick_alive = 10
        self.tick_speed = self.tick_alive
        self.index = 1
        self.dead_index = 1
        self.dead_timer = 1
        self.directions_remain = []
        self.alive = True
        self.eat = False
        self.timer = pygame.time.get_ticks()

    def update(self, maze, screen, pm):
        if gf.ball_stop(self, maze) is False and pygame.time.get_ticks() - self.timer >= self.tick_speed:
            self.timer = pygame.time.get_ticks()
            if self.move == "l":
                self.image.rect.x -= self.speed
                if self.eat is False:
                    file = "pink_left_" + str(math.floor(self.index))
                else:
                    file = "eyes_left"
            elif self.move == "r":
                self.image.rect.x += self.speed
                if self.eat is False:
                    file = "pink_right_" + str(math.floor(self.index))
                else:
                    file = "eyes_right"
            elif self.move == "d":
                self.image.rect.y += self.speed
                if self.eat is False:
                    file = "pink_down_" + str(math.floor(self.index))
                else:
                    file = "eyes_down"
            elif self.move == "u":
                self.image.rect.y -= self.speed
                if self.eat is False:
                    file = "pink_up_" + str(math.floor(self.index))
                else:
                    file = "eyes_up"
            else:
                file = "pink_left_1"
            self.image = ImageRect(screen, file, 30, 30)
            self.image.rect = self.rect
            if self.index > 2.5:
                self.index = 1
            else:
                self.index += .1

        if self.alive is False and self.eat is False:
            file = "blink_" + str(math.floor(self.dead_index))
            self.image = ImageRect(screen, file, 30, 30)
            self.image.rect = self.rect
            if self.dead_timer > 20:
                self.alive = True
            else:
                self.dead_timer += .05
                if self.dead_timer < 15:
                    if self.dead_index > 2.5:
                        self.dead_index = 1
                    else:
                        self.dead_index += .1
                else:
                    if self.dead_index > 3.5:
                        self.dead_index = 2
                    else:
                        self.dead_index += .1

        if self.alive is True:
            self.tick_speed = self.tick_alive
        elif self.alive is False:
            self.tick_speed = self.tick_dead

        self.self_movement(maze)
        self.dead_collide(pm, maze)

    def self_movement(self, maze):
        if self.move == "u" and self.rect == (300, 230, 30, 30):
            self.move = "l"

        elif 295 < self.rect.x < 305 and 325 < self.rect.y < 335:
            self.move = "u"

        if gf.ball_stop(self, maze) is True and self.eat is False:
            self.check_directions(maze)
            if len(self.directions_remain) == 0:
                self.move = "l"
                self.move = "r"
                self.move = "u"
                self.move = "d"
            else:
                rand = random.choice(self.directions_remain)
                self.move = rand

        if self.eat is True:
            self.check_directions(maze)

            if self.rect.x < 190 and self.rect.y is not 230:
                if "r" in self.directions_remain:
                    self.move = "r"
                elif gf.ball_stop(self, maze):
                    rand = random.choice(self.directions_remain)
                    self.move = rand

            elif self.rect.x > 410 and self.rect.y is not 230:
                if "l" in self.directions_remain:
                    self.move = "l"
                elif gf.ball_stop(self, maze):
                    rand = random.choice(self.directions_remain)
                    self.move = rand

            elif self.rect.y < 230 and self.rect.x is not 300:
                if "d" in self.directions_remain:
                    self.move = "d"
                elif gf.ball_stop(self, maze):
                    rand = random.choice(self.directions_remain)
                    self.move = rand

            elif self.rect.y > 230 and self.rect.x is not 300:
                if "u" in self.directions_remain:
                    self.move = "u"
                elif gf.ball_stop(self, maze):
                    rand = random.choice(self.directions_remain)
                    self.move = rand

            elif self.rect.y is 230 and 190 < self.rect.x < 410:
                if 295 < self.rect.x < 305:
                    self.move = "d"
                elif self.rect.x < 300:
                    self.move = "r"
                elif self.rect.x > 300:
                    self.move = "l"
            else:
                rand = random.choice(self.directions_remain)
                self.move = rand

    def check_directions(self, maze):
        self.directions_remain.clear()
        self.direction = "u"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "d":
                self.directions_remain.append("u")

        self.direction = "d"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "u":
                self.directions_remain.append("d")

        self.direction = "l"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "r":
                self.directions_remain.append("l")

        self.direction = "r"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "l":
                self.directions_remain.append("r")

    def blitme(self):
        self.image.blitme()

    def dead_collide(self, pm, maze):
        if pygame.sprite.collide_rect(self, pm) and self.alive is False:
            if self.alive is False and self.eat is False:
                pm.score += 200
                eat = pygame.mixer.Sound('sounds/eatghost.wav')
                eat.play()
                self.eat = True

        if self.eat is True:
            for lines in maze.lines:
                if lines.colliderect(self):
                    self.eat = False
                    self.alive = True


class OrangeGhost(Sprite):

    def __init__(self, screen, maze):
        super(OrangeGhost, self).__init__()
        self.screen = screen.get_rect()
        self.image = ImageRect(screen, "orange_left_1", 30, 30)
        self.rect = self.image.rect
        self.rect.x = 350
        self.rect.y = 330
        self.maze = maze
        self.direction = "u"
        self.move = "u"
        self.speed = 5
        self.tick_dead = 30
        self.tick_alive = 10
        self.tick_speed = self.tick_alive
        self.index = 1
        self.dead_index = 1
        self.dead_timer = 1
        self.directions_remain = []
        self.alive = True
        self.eat = False
        self.timer = pygame.time.get_ticks()

    def update(self, maze, screen, pm):
        if gf.ball_stop(self, maze) is False and pygame.time.get_ticks() - self.timer >= self.tick_speed:
            self.timer = pygame.time.get_ticks()
            if self.move == "l":
                self.image.rect.x -= self.speed
                if self.eat is False:
                    file = "orange_left_" + str(math.floor(self.index))
                else:
                    file = "eyes_left"
            elif self.move == "r":
                self.image.rect.x += self.speed
                if self.eat is False:
                    file = "orange_right_" + str(math.floor(self.index))
                else:
                    file = "eyes_right"
            elif self.move == "d":
                self.image.rect.y += self.speed
                if self.eat is False:
                    file = "orange_down_" + str(math.floor(self.index))
                else:
                    file = "eyes_down"
            elif self.move == "u":
                self.image.rect.y -= self.speed
                if self.eat is False:
                    file = "orange_up_" + str(math.floor(self.index))
                else:
                    file = "eyes_up"
            else:
                file = "orange_left_1"
            self.image = ImageRect(screen, file, 30, 30)
            self.image.rect = self.rect
            if self.index > 2.5:
                self.index = 1
            else:
                self.index += .1

        if self.alive is False and self.eat is False:
            file = "blink_" + str(math.floor(self.dead_index))
            self.image = ImageRect(screen, file, 30, 30)
            self.image.rect = self.rect
            if self.dead_timer > 20:
                self.alive = True
            else:
                self.dead_timer += .05
                if self.dead_timer < 15:
                    if self.dead_index > 2.5:
                        self.dead_index = 1
                    else:
                        self.dead_index += .1
                else:
                    if self.dead_index > 3.5:
                        self.dead_index = 2
                    else:
                        self.dead_index += .1

        if self.alive is True:
            self.tick_speed = self.tick_alive
        elif self.alive is False:
            self.tick_speed = self.tick_dead

        self.self_movement(maze)
        self.dead_collide(pm, maze)

    def self_movement(self, maze):
        if self.move == "u" and self.rect == (300, 230, 30, 30):
            self.move = "l"

        elif 295 < self.rect.x < 305 and 325 < self.rect.y < 335:
            self.move = "u"

        if gf.ball_stop(self, maze) is True and self.eat is False:
            self.check_directions(maze)
            if len(self.directions_remain) == 0:
                self.move = "l"
                self.move = "r"
                self.move = "u"
                self.move = "d"
            else:
                rand = random.choice(self.directions_remain)
                self.move = rand

        if self.eat is True:
            self.check_directions(maze)

            if self.rect.x < 190 and self.rect.y is not 230:
                if "r" in self.directions_remain:
                    self.move = "r"
                elif gf.ball_stop(self, maze):
                    rand = random.choice(self.directions_remain)
                    self.move = rand

            elif self.rect.x > 410 and self.rect.y is not 230:
                if "l" in self.directions_remain:
                    self.move = "l"
                elif gf.ball_stop(self, maze):
                    rand = random.choice(self.directions_remain)
                    self.move = rand

            elif self.rect.y < 230 and self.rect.x is not 300:
                if "d" in self.directions_remain:
                    self.move = "d"
                elif gf.ball_stop(self, maze):
                    rand = random.choice(self.directions_remain)
                    self.move = rand

            elif self.rect.y > 230 and self.rect.x is not 300:
                if "u" in self.directions_remain:
                    self.move = "u"
                elif gf.ball_stop(self, maze):
                    rand = random.choice(self.directions_remain)
                    self.move = rand

            elif self.rect.y is 230 and 190 < self.rect.x < 410:
                if 295 < self.rect.x < 305:
                    self.move = "d"
                elif self.rect.x < 300:
                    self.move = "r"
                elif self.rect.x > 300:
                    self.move = "l"
            else:
                rand = random.choice(self.directions_remain)
                self.move = rand

    def check_directions(self, maze):
        self.directions_remain.clear()
        self.direction = "u"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "d":
                self.directions_remain.append("u")

        self.direction = "d"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "u":
                self.directions_remain.append("d")

        self.direction = "l"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "r":
                self.directions_remain.append("l")

        self.direction = "r"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "l":
                self.directions_remain.append("r")

    def blitme(self):
        self.image.blitme()

    def dead_collide(self, pm, maze):
        if pygame.sprite.collide_rect(self, pm) and self.alive is False:
            if self.alive is False and self.eat is False:
                pm.score += 200
                eat = pygame.mixer.Sound('sounds/eatghost.wav')
                eat.play()
                self.eat = True

        if self.eat is True:
            for lines in maze.lines:
                if lines.colliderect(self):
                    self.eat = False
                    self.alive = True
