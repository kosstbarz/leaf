import pygame

from leaf.core import tile, game


class Controller:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        self.clock = pygame.time.Clock()
        self.game_ = game.Game()

    def main_loop(self):
        terminated = False
        shift = [50., 50.]
        self.game_.shift(tuple(shift))
        while not terminated:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminated = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    shift[1] -= 10
                    self.game_.shift(tuple(shift))
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    shift[1] += 10
                    self.game_.shift(tuple(shift))
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    shift[0] += 10
                    self.game_.shift(tuple(shift))
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    shift[0] -= 10
                    self.game_.shift(tuple(shift))
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.game_.pause = not self.game_.pause

            self.game_.update()
            self.game_.render(self.screen)
            self.clock.tick(50)
        pygame.display.quit()
