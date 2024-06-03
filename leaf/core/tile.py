from __future__ import annotations

import math
from typing import Tuple

import pygame
from pygame import freetype

from leaf.tiles import default


def get_minimal_radius(radius) -> float:
    """Horizontal length of the hexagon"""
    # https://en.wikipedia.org/wiki/Hexagon#Parameters
    return radius * math.cos(math.radians(30))


def highlight_colour(colour, offset) -> Tuple[int, ...]:
    """Colour of the hexagon tile when rendering highlight"""
    brighten = lambda x, y: x + y if x + y < 255 else 255
    return tuple(brighten(x, offset) for x in colour)


class Tile:

    def __init__(self, position: tuple[int, int], radius: float = 50, init_food=10):
        self.font = freetype.SysFont('Comic Sans MS', 20)
        self.owner = None
        self.food = init_food
        self.rot = 0
        self.type = default.Default()

        self.radius = radius
        self.position = position
        self.highlight_offset: int = 3
        self.max_highlight_ticks: int = 15
        self.highlight_tick = 0
        self.shift = (0, 0)
        self.border = 5
        self.owner_width = 10
        self.vertices = self.compute_vertices(self.radius - self.border)
        self.is_border = False
        self.influence = {}

    def visual_update(self):
        """Updates tile highlights"""
        if self.highlight_tick > 0:
            self.highlight_tick -= 1

    def update(self):
        self.type.update(self)

    def make_shift(self, shift: tuple[float, float]):
        self.shift = shift
        self.vertices = self.compute_vertices(self.radius - self.border)

    def compute_vertices(self, radius) -> list[tuple[float, float]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""
        # pylint: disable=invalid-name
        half_radius = radius / 2
        minimal_radius = get_minimal_radius(radius)
        center_x, center_y = self.centre
        return [
            (center_x, center_y - radius),
            (center_x - minimal_radius, center_y - half_radius),
            (center_x - minimal_radius, center_y + half_radius),
            (center_x, center_y + radius),
            (center_x + minimal_radius, center_y + half_radius),
            (center_x + minimal_radius, center_y - half_radius),
        ]

    def collide_with_point(self, point: Tuple[float, float]) -> bool:
        """Returns True if distance from centre to point is less than horizontal_length"""
        return math.dist(point, self.centre) < get_minimal_radius(self.radius - self.border)

    def _render(self, screen, main_color):
        pygame.draw.polygon(screen, main_color, self.vertices)
        text_surface, rect = self.font.render(str(self.food), (0, 0, 0))
        x, y = self.centre
        if self.owner is not None:
            pygame.draw.polygon(screen, self.owner.color, self.vertices)
            pygame.draw.polygon(screen, main_color,
                                self.compute_vertices(self.radius - self.border - self.owner_width))
        screen.blit(text_surface, (int(x - rect.width / 2), y - rect.height))

    def render(self, screen) -> None:
        """Renders the hexagon on the screen"""
        self._render(screen, self.type.color)

    def render_highlight(self, screen, border_colour) -> None:
        """Draws a border around the hexagon with the specified colour"""
        if self.owner is None:
            return
        self.highlight_tick = self.max_highlight_ticks
        self._render(screen, highlight_colour(self.type.color, self.highlight_offset * self.highlight_tick))
        pygame.draw.aalines(screen, border_colour, closed=True, points=self.vertices)

    @property
    def centre(self) -> Tuple[float, float]:
        """Centre of the hexagon"""
        id_x, id_y = self.position
        half_radius = self.radius / 2
        minimal_radius = get_minimal_radius(self.radius)
        center_x = 2 * id_x * minimal_radius + self.shift[0]
        center_y = id_y * (self.radius + half_radius) + self.shift[1]
        if id_y % 2 == 1:
            center_x = center_x + minimal_radius
        return center_x, center_y

