import pygame

from leaf.core import game
from leaf.gui import build_panel, control_panel


class Controller:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        self.clock = pygame.time.Clock()
        self.game_ = game.Game()
        self.build_panel = build_panel.Panel()
        self.control_panel = control_panel.Panel()

    def main_loop(self):
        terminated = False
        shift = [50., 50.]
        self.game_.shift(tuple(shift))
        while not terminated:
            events = pygame.event.get()
            for event in events:
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # left button
                        if not self.build_panel.check_click():
                            if not self.control_panel.check_click():
                                tile_ = self.game_.left_click()
                                self.build_panel.update_active_tile(tile_)
                                self.control_panel.update_active_tile(tile_)
                    elif event.button == 3: # right button
                        self.game_.right_click()

            self.game_.update()
            self.game_.render(self.screen)
            self.build_panel.render(self.screen)
            self.control_panel.render(self.screen)
            pygame.display.flip()
            self.clock.tick(50)
        pygame.display.quit()
