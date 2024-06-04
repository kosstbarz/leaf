import enum

import pygame

from leaf.core import direction, tile
from leaf.gui import geometry
from leaf.tiles import base

FOOD_FOR_BUTTON = 10
RENDER_LENGTH = 0.4
RENDER_THICK = 3
RENDER_COLOR = (5, 5, 5)
DIRECTION_LIMIT = 4

class Vein(base.Base):
    color = (100, 100, 150)
    produce_food = -3

    def __init__(self):
        super().__init__()
        self.open_directions = set()

    def get_penetration(self, ferment_id, direction) -> float:
        if ferment_id == 0:
            if direction in self.open_directions:
                return 2
            else:
                return 0.01
        if direction in self.open_directions:
            return 1
        else:
            return 0.1

    def limit(self, ferment_id) -> int:
        return 100

    def render(self, screen, tile_):
        x_center, y_center = tile_.centre
        r = tile.get_minimal_radius(tile_.radius)
        vertices = [
            (x_center - r, y_center - RENDER_THICK),
            (x_center - r * (1 - RENDER_LENGTH),  y_center - RENDER_THICK),
            (x_center - r * (1 - RENDER_LENGTH), y_center + RENDER_THICK),
            (x_center - r, y_center + RENDER_THICK),
        ]
        angles = [60, 120, 180, -120, -60, 0]
        for direct in self.open_directions:
            angle = angles[direct.value]
            rot_vert = []
            for vert in vertices:
                rot_vert.append(geometry.rotate_point_relative(vert[0], vert[1], x_center, y_center, angle))
            pygame.draw.polygon(screen, RENDER_COLOR, rot_vert)

    def render_highlight(self, screen, tile_):
        x_center, y_center = tile_.centre
        r = tile.get_minimal_radius(tile_.radius)
        vertices = [
            (x_center - r, y_center - RENDER_THICK),
            (x_center - r * (1 - RENDER_LENGTH), y_center - RENDER_THICK),
            (x_center - r * (1 - RENDER_LENGTH), y_center + RENDER_THICK),
            (x_center - r, y_center + RENDER_THICK),
        ]
        angles = [60, 120, 180, -120, -60, 0]
        for direct in self.open_directions:
            angle = angles[direct.value]
            rot_vert = []
            for vert in vertices:
                rot_vert.append(geometry.rotate_point_relative(vert[0], vert[1], x_center, y_center, angle))
            pygame.draw.polygon(screen, RENDER_COLOR, rot_vert)

    def right_click(self, cur_tile, clicked_tile):
        direct = direction.get_direction(cur_tile, clicked_tile)
        if direct is None:
            return
        if cur_tile.ferments[0] >= FOOD_FOR_BUTTON:
            if direct in self.open_directions:
                self.open_directions.remove(direct)
            else:
                if len(self.open_directions) >= DIRECTION_LIMIT:
                    return
                self.open_directions.add(direct)
                print(f"Added direction {direct}")
            self.add_ferment(cur_tile, 0, -FOOD_FOR_BUTTON)
