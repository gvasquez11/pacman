import sys
import pygame


def update_screen(screen, pman, red_ghost, blue_ghost, pink_ghost, orange_ghost, maze, stats, display):
    if stats.start_screen is False:
        screen.fill((0, 0, 0))
        maze.blitme()
        display.score_blit(screen, stats, pman)
        pman.blitme()

        if stats.get_ready and stats.start_screen is False:
            stats.ready()
            red_ghost.blitme()
            blue_ghost.blitme()
            pink_ghost.blitme()
            orange_ghost.blitme()

        if not stats.game_pause and not stats.game_over and not stats.get_ready:
            pman.update(maze, screen)
            red_ghost.blitme()
            red_ghost.update(maze, screen, pman)
            blue_ghost.blitme()
            blue_ghost.update(maze, screen, pman)
            pink_ghost.blitme()
            pink_ghost.update(maze, screen, pman)
            orange_ghost.blitme()
            orange_ghost.update(maze, screen, pman)

    elif stats.start_screen is True:
        display.start(screen, stats)

        pygame.display.flip()


def check_events(screen, pman, red_ghost, blue_ghost, pink_ghost, orange_ghost, maze, stats, dispaly):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()
            elif event.key == pygame.K_LEFT:
                pman.direction_l = True
            elif event.key == pygame.K_RIGHT:
                pman.direction_r = True
            elif event.key == pygame.K_UP:
                pman.direction_u = True
            elif event.key == pygame.K_DOWN:
                pman.direction_d = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                pman.direction_l = False
            elif event.key == pygame.K_RIGHT:
                pman.direction_r = False
            elif event.key == pygame.K_UP:
                pman.direction_u = False
            elif event.key == pygame.K_DOWN:
                pman.direction_d = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            dispaly.button_clicks(pman, stats, maze)

    pman_ball_collision(pman, maze)
    check_movement(pman, maze)
    power_up(pman, maze, red_ghost, blue_ghost, pink_ghost, orange_ghost)
    pman.ghost_collision(red_ghost, blue_ghost, pink_ghost, orange_ghost, stats, screen)
    stats.update_txt(pman)


def check_movement(pman, maze):
    if pman.direction_l is True:
        pman.direction = "l"
        if brick_collision(pman, maze) is False:
            pman.move = "l"
    elif pman.direction_r is True:
        pman.direction = "r"
        if brick_collision(pman, maze) is False:
            pman.move = "r"
    elif pman.direction_u is True:
        pman.direction = "u"
        if brick_collision(pman, maze) is False:
            pman.move = "u"
    elif pman.direction_d is True:
        pman.direction = "d"
        if brick_collision(pman, maze) is False:
            pman.move = "d"


def brick_collision(pman, maze):
    if pman.direction == "l":
        temp = pman.rect.move(-1, 0)
    elif pman.direction == "r":
        temp = pman.rect.move(1, 0)
    elif pman.direction == "u":
        temp = pman.rect.move(0, -1)
    elif pman.direction == "d":
        temp = pman.rect.move(0, 1)
    else:
        temp = pman.rect.move(0, 0)

    for brick in maze.bricks:
        if brick.colliderect(temp):
            return True

    return False


def ball_stop(pman, maze):
    if pman.move == "l":
        temp = pman.rect.move(-1, 0)
    elif pman.move == "r":
        temp = pman.rect.move(1, 0)
    elif pman.move == "u":
        temp = pman.rect.move(0, -1)
    elif pman.move == "d":
        temp = pman.rect.move(0, 1)
    else:
        temp = pman.rect.move(0, 0)

    for brick in maze.bricks:
        if brick.colliderect(temp):
            return True

    return False


def pman_ball_collision(pman, maze):
    for balls in maze.balls:
        if balls.colliderect(pman):
            maze.balls.remove(balls)
            pman.score += 10

            if pman.sound_index >= 2:
                pman.sound_index = 1
                chomp = pygame.mixer.Sound('sounds/chomp.wav')
                chomp.play()
            else:
                pman.sound_index += .3


def power_up(pman, maze, redghost, blueghost, pinkghost, orangeghost):
    for power_up_balls in maze.power_up_balls:
        if power_up_balls.colliderect(pman):
            maze.power_up_balls.remove(power_up_balls)
            redghost.alive = False
            redghost.dead_timer = 1
            blueghost.alive = False
            blueghost.dead_timer = 1
            pinkghost.alive = False
            pinkghost.dead_timer = 1
            orangeghost.alive = False
            orangeghost.dead_timer = 1


def reset(pman, redghost, blueghost, pinkghost, orangeghost, stats):
    pman.rect.x = pman.screen.centerx - 10
    pman.rect.y = pman.screen.centery + 110
    pman.move = "l"

    redghost.rect.x = 300
    redghost.rect.y = 230
    blueghost.rect.x = 250
    blueghost.rect.y = 330
    pinkghost.rect.x = 300
    pinkghost.rect.y = 330
    orangeghost.rect.x = 350
    orangeghost.rect.y = 330

    if stats.game_over is False:
        stats.get_ready = True
