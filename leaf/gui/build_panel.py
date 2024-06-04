import pygame
from pygame import freetype

from leaf.core import tile
from leaf.tiles import source, storage, vein

BUTTON_HEIGHT = 40
BUTTON_WIDTH = 150
BUTTON_GAP = 10
CORNER_GAP_RIGHT = 30
CORNER_GAP_DOWN = 30
BUTTONS = {
    "PRODUCER": source.Source,
    "STORAGE": storage.Storage,
    "VEIN": vein.Vein,
}

class Panel:
    def __init__(self):
        self.active_tile = None
        self.rects = {}
        self.font = freetype.SysFont('Corbel', 25)
        self.color_light = (170, 170, 170)
        self.color_dark = (150, 150, 150)

    def check_click(self):
        print("In click")
        if not self.active:
            print("Not active")
            return False
        mouse = pygame.mouse.get_pos()
        print(f"Rects {self.rects}, point {mouse}")
        for name, rect in self.rects.items():
            if rect.collidepoint(mouse):
                print("Collision")
                self.active_tile.change_type(BUTTONS[name])
                return True
        print("No colision")
        return False

    def update_active_tile(self, tile_: tile.Tile):
        self.active_tile = tile_
        print(f"Active tile updated {self.active_tile}")

    def render(self, screen):
        self.rects = {}
        if not self.active:
            return
        # print("Render panel")
        needed_buttons = [name for name, type in BUTTONS.items() if not isinstance(self.active_tile.type, BUTTONS[name])]
        # print(f"Needed {needed_buttons}")
        mouse = pygame.mouse.get_pos()
        size_x = BUTTON_WIDTH
        size_y = len(needed_buttons) * BUTTON_HEIGHT + (len(needed_buttons) - 1) * BUTTON_GAP
        corner_x = screen.get_width() - size_x - CORNER_GAP_RIGHT
        corner_y = screen.get_height() - size_y - CORNER_GAP_DOWN
        for button in needed_buttons:
            button_rect = pygame.Rect(corner_x, corner_y, BUTTON_WIDTH, BUTTON_HEIGHT)
            if button_rect.collidepoint(mouse):
                pygame.draw.rect(screen, self.color_light, button_rect)
            else:
                pygame.draw.rect(screen, self.color_dark, button_rect)
            text_surface, rect = self.font.render(button, (0, 0, 0))
            screen.blit(text_surface, (corner_x + 10, corner_y + 10))
            self.rects[button] = button_rect
            corner_y += BUTTON_HEIGHT + BUTTON_GAP

    @property
    def active(self) -> bool:
        return self.active_tile is not None
