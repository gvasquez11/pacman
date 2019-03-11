import pygame
from image_rect import ImageRect


class Maze:
    STANDARD_SIZE = 10

    def __init__(self, screen, mazefile):
        self.screen = screen
        self.filename = mazefile

        # load the maze txt file
        with open('/Users/gregoryvasquez/PycharmProjects/pacman/maze.txt', 'r') as f:
            self.rows = f.readlines()

        # create arrays and upload images for block, ball, line(walls), and power up balls
        self.bricks = []
        self.brick = ImageRect(screen, "wall", Maze.STANDARD_SIZE, Maze.STANDARD_SIZE)
        self.balls = []
        self.ball = ImageRect(screen, "ball", Maze.STANDARD_SIZE, Maze.STANDARD_SIZE)
        self.lines = []
        self.line = ImageRect(screen, "line", Maze.STANDARD_SIZE, Maze.STANDARD_SIZE)
        self.power_up_balls = []
        self.power_up_ball = ImageRect(screen, "powerUp", 12, 12)
        self.build()

    def __str__(self):
        return 'maze( ' + self.filename + ')'

    def build(self):
        r = self.brick.rect
        w, h = r.width, r.height

        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == 'x':
                    self.bricks.append(pygame.Rect(ncol * Maze.STANDARD_SIZE, nrow * Maze.STANDARD_SIZE, w, h))
                if col == 'p':
                    self.power_up_balls.append(pygame.Rect(ncol * Maze.STANDARD_SIZE, nrow * Maze.STANDARD_SIZE, w, h))
                if col == '*':
                    self.balls.append(pygame.Rect(ncol * Maze.STANDARD_SIZE, nrow * Maze.STANDARD_SIZE, w, h))
                if col == '-':
                    self.lines.append(pygame.Rect(ncol * Maze.STANDARD_SIZE, nrow * Maze.STANDARD_SIZE, w, h))

    def blitme(self):
        for rect in self.bricks:
            self.screen.blit(self.brick.image, rect)
        for rect in self.power_up_balls:
            self.screen.blit(self.power_up_ball.image, rect)
        for rect in self.balls:
            self.screen.blit(self.ball.image, rect)
        for rect in self.lines:
            self.screen.blit(self.line.image, rect)
