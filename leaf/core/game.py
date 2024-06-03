import pygame
from pygame import freetype

from leaf.core import board, player


class Game:
    def __init__(self):
        self.player = player.Player((100, 100, 20))
        self.board_ = board.Board(width=4, height=4, player=self.player)
        self.prev_update = 0
        self.delay = 2000
        self.pause = False
        self.font = freetype.SysFont('Comic Sans MS', 50)

    def update(self):
        if pygame.time.get_ticks() - self.prev_update > self.delay and not self.pause:
            self.board_.update()
            self.prev_update = pygame.time.get_ticks()
        self.board_.visual_update()

    def render(self, screen):
        self.board_.render(screen)
        if self.pause:
            text_surface, rect = self.font.render("PAUSED", (0, 0, 0))
            screen.blit(text_surface, (300, 200))
        pygame.display.flip()

    def shift(self, shift: tuple[float, float]):
        self.board_.shift(shift)
