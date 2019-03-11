import pygame


class Stats:

    def __init__(self):
        self.start_screen = True
        self.game_active = True
        self.game_pause = False
        self.game_over = False
        self.get_ready = True
        self.index = 0
        self.high_score = 0
        self.first_sound = True
        self.first_time = True
        self.wr = open('highscore.txt', 'r+')
        self.current = int(self.wr.read())

    def ready(self):
        if self.first_time is True:
            if self.first_sound is True:
                begin = pygame.mixer.Sound('sounds/beginning.wav')
                begin.play()
                self.first_sound = False
            if self.index >= 50:
                self.index = 0
                self.get_ready = False
                self.first_time = False
            else:
                self.index += .3

        elif self.first_time is False:
            if self.index >= 20:
                self.index = 0
                self.get_ready = False
            else:
                self.index += .3

    def update_txt(self, pman):
        self.wr.seek(0)
        self.current = int(self.wr.read())
        self.high_score = self.current
        if self.current < pman.score:
            self.wr.seek(0)
            self.wr.truncate()
            self.wr.write(str(pman.score))
