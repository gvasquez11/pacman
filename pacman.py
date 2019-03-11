import pygame
import game_functions as gf
from maze import Maze
from pman import PMAN
from stats import Stats
from display import Display
from ghosts import RedGhost, BlueGhost, PinkGhost, OrangeGhost


def run_game():

    pygame.init()
    screen = pygame.display.set_mode((630, 800))
    pygame.display.set_caption("Portal Pac-Man")

    mazefile = 'maze.txt'
    maze = Maze(screen, mazefile)

    pman = PMAN(screen, maze)
    stats = Stats()
    rghost = RedGhost(screen, maze)
    bghost = BlueGhost(screen, maze)
    pghost = PinkGhost(screen, maze)
    oghost = OrangeGhost(screen, maze)

    display = Display(screen, pman)

    while True:
        gf.check_events(screen, pman, rghost, bghost, pghost, oghost, maze, stats, display)
        gf.update_screen(screen, pman, rghost, bghost, pghost,oghost, maze, stats, display)
        pygame.display.flip()


run_game()
