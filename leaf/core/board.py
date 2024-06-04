import math

import numpy as np
import pygame

from leaf.core import tile, direction
from leaf.tiles import source, dead

INFLUENCE_TO_CAPTURE = 50
INFLUENCE_HISTORY = 10
CAPTURE_FOOD_LOST = 300


class Board:
    def __init__(self, width: int, height: int, player):
        self.width = width
        self.height = height
        self.tiles: list[list[tile.Tile]] = []
        for w in range(width):
            column = []
            self.tiles.append(column)
            for h in range(height):
                column.append(tile.Tile((w, h)))
        self.tiles[0][0].owner = player
        self.tiles[0][0].type = source.Source()
        for column in self.tiles:
            for tile_ in column:
                tile_.is_border = self.is_border(tile_)
        self.active_tile = None

    def is_border(self, tile_: tile.Tile) -> bool:
        owners = [t.owner for t in self.compute_neighbours(tile_)]
        return any([ow != tile_.owner for ow in owners])

    def compute_neighbours(self, tile_: tile.Tile) -> list[tile.Tile]:
        """Returns tiles whose indexes are close"""
        id_x, id_y = tile_.position

        neighbour_ids = []
        if id_y % 2 == 0:
            for direct in direction.Dir:
                diff = direction.neighbour_ids_even[direct.value]
                neighbour_ids.append((id_x + diff[0], id_y + diff[1]))
        else:
            for direct in direction.Dir:
                diff = direction.neighbour_ids_odd[direct.value]
                neighbour_ids.append((id_x + diff[0], id_y + diff[1]))

        # print(neighbour_ids)
        neighbours = [self.tiles[idx][idy] for idx, idy in neighbour_ids if idx >= 0 and idx < self.width and idy >= 0 and idy < self.height]
        # print(neighbours)
        return neighbours

    def visual_update(self):
        for column in self.tiles:
            for tile in column:
                tile.visual_update()

    def give_ferment(self, ferment_id: int, tile1: tile.Tile, tile2: tile.Tile, direction_, want_to_change):
        diff = tile1.visible_ferments[ferment_id] - tile2.visible_ferments[ferment_id]
        if diff == 0:
            return
        penetration_sq = tile1.type.get_penetration(ferment_id, direction_) * tile2.type.get_penetration(ferment_id, direction_.opposite())
        if penetration_sq <= 0:
            return
        a = int(diff * math.sqrt(penetration_sq) / 12)
        idx, idy = tile1.position
        want_to_change[idx, idy, direction_.value] = a
        if a > 50:
            print(f"{ferment_id=}, {tile1.position}, {tile2.position}, {diff=}, {math.sqrt(penetration_sq)=}, {a=}")
        idx1, idy1 = tile2.position
        want_to_change[idx1, idy1, direction_.opposite().value] = -a
        # assert np.sum(want_to_change) == 0, f"to change is incorrect: {np.sum(want_to_change)}\n{tile2.food} {tile.food} {diff} {tile.position} {tile2.position}\n{[tile_.food for col in self.tiles for tile_ in col]}\n{want_to_change}"

    def exchange(self, ferment_id: int):
        want_to_change = np.zeros((self.width, self.height, 6), dtype=int)
        for column in self.tiles:
            for tile in column:
                idx, idy = tile.position
                if idx < self.width - 1:
                    self.give_ferment(ferment_id, tile, self.tiles[idx + 1][idy], direction.Dir.RIGHT, want_to_change)
                if idy % 2 == 0:
                    if idy < self.height - 1:
                        self.give_ferment(ferment_id, tile, self.tiles[idx][idy + 1], direction.Dir.DOWN_RIGHT, want_to_change)
                    if idy < self.height - 1 and idx > 0:
                        self.give_ferment(ferment_id, tile, self.tiles[idx - 1][idy + 1], direction.Dir.DOWN_LEFT, want_to_change)
                else:
                    if idy < self.height - 1 and idx < self.width - 1:
                        self.give_ferment(ferment_id, tile, self.tiles[idx + 1][idy + 1], direction.Dir.DOWN_RIGHT, want_to_change)
                    if idy < self.height - 1:
                        self.give_ferment(ferment_id, tile, self.tiles[idx][idy + 1], direction.Dir.DOWN_LEFT, want_to_change)

        # apply give limit
        for idx, row in enumerate(want_to_change):
            for idy, tile_ in enumerate(row):
                limit = min(self.tiles[idx][idy].type.limit(ferment_id), self.tiles[idx][idy].ferments[ferment_id])
                if np.sum(np.maximum(tile_, 0)) > limit:
                    coef = np.sum(np.maximum(tile_, 0)) / limit
                    for idd, v in enumerate(tile_):
                        if v > 0:
                            want_to_change[idx, idy, idd] = int(v / coef)
                            idx1, idy1 = direction.get_index(idx, idy, idd)
                            want_to_change[idx1, idy1, (idd+3) % 6] = int(-v / coef)
                            # print(np.sum(np.maximum(tile, 0)), self.tiles[idx][idy].type.limit(),coef, want_to_change )

        assert np.sum(want_to_change) == 0, f"Want to change is incorrect: {np.sum(want_to_change)}\n{want_to_change}"

        # make exchange and calc influence
        for column in self.tiles:
            for tile_ in column:
                idx, idy = tile_.position
                gave = np.sum(want_to_change[idx, idy])
                if gave > tile_.ferments[ferment_id]:
                    print(f"{idx=}, {idy=}, {gave=}, {tile_.ferments[ferment_id]=}")
                tile_.add_ferments(ferment_id, -gave)
                if tile_.is_border and ferment_id == 0:
                    new_inf = {key: 0 for key in tile_.influence.keys()}
                    for idd, d in enumerate(want_to_change[idx, idy]):
                        if d < 0:
                            idx_1, idy_1 = direction.get_index(idx, idy, idd)
                            owner = self.tiles[idx_1][idy_1].owner
                            if owner not in new_inf:
                                new_inf[owner] = 0
                            new_inf[owner] -= d
                    for owner, infl in new_inf.items():
                        if owner not in tile_.influence:
                            tile_.influence[owner] = []
                        tile_.influence[owner].append(infl)
                        if len(tile_.influence[owner]) > INFLUENCE_HISTORY:
                            tile_.influence[owner].pop(0)

    def calc_rotten(self):
        for column in self.tiles:
            for tile_ in column:
                if tile_.ferments[1] >= tile_.type.rot_max:
                    tile_.type = dead.Dead()
                    tile_.owner = None
                    tile_.ferments = [0, 0]
                    tile_.visible_ferments = [0, 0]

    def calc_capture(self):
        for column in self.tiles:
            for tile_ in column:
                if tile_.is_border:
                    best, second = 0, 0
                    best_owner = None
                    for owner, infl in tile_.influence.items():
                        if sum(infl) > best:
                            second = best
                            best = sum(infl)
                            best_owner = owner
                    if best - second > INFLUENCE_TO_CAPTURE and best_owner != tile_.owner:
                        tile_.owner = best_owner
                        tile_.influence = {}
                        tile_.ferments[0] = max(tile_.ferments[0] - CAPTURE_FOOD_LOST, 0)
                        for neighbour in self.compute_neighbours(tile_):
                            neighbour.is_border = self.is_border(neighbour)

        # print(want_to_change[0,0])

    def update(self):
        for column in self.tiles:
            for tile_ in column:
                tile_.update()

        for i in tile.Ferment:
            self.exchange(i.value)
        self.calc_rotten()
        self.calc_capture()

    def shift(self, shift):
        for column in self.tiles:
            for tile_ in column:
                tile_.make_shift(shift=shift)

    def left_click(self):
        mouse_pos = pygame.mouse.get_pos()
        clicked_tile = None
        for column in self.tiles:
            if clicked_tile is not None:
                break
            for tile in column:
                if tile.collide_with_point(mouse_pos):
                    if tile.owner is not None:
                        clicked_tile = tile
                        self.active_tile = clicked_tile
                    return clicked_tile
        self.active_tile = clicked_tile
        return clicked_tile

    def right_click(self):
        if self.active_tile is None:
            return None
        right_click = getattr(self.active_tile.type, "right_click", None)
        if not callable(right_click):
            return None
        mouse_pos = pygame.mouse.get_pos()
        clicked_tile = None
        for column in self.tiles:
            if clicked_tile is not None:
                break
            for tile_ in column:
                if tile_.collide_with_point(mouse_pos):
                    clicked_tile = tile_
                    break
        if clicked_tile is not None:
            right_click(self.active_tile, clicked_tile)

    def render(self, screen):
        """Renders hexagons on the screen"""
        screen.fill((200, 200, 200))
        for column in self.tiles:
            for tile in column:
                tile.render(screen)

        if self.active_tile:
            self.active_tile.render_highlight(screen, border_colour=(0, 0, 0))
        # draw borders around colliding hexagons and neighbours
        # mouse_pos = pygame.mouse.get_pos()
        # colliding_hexagon = None
        # for column in self.tiles:
        #     if colliding_hexagon is not None:
        #         break
        #     for tile in column:
        #         if tile.collide_with_point(mouse_pos):
        #             colliding_hexagon = tile
        #             break
        # if colliding_hexagon is not None:
        #     # for neighbour in self.compute_neighbours(colliding_hexagon):
        #     #     neighbour.render_highlight(screen, border_colour=(100, 100, 100))
        #     colliding_hexagon.render_highlight(screen, border_colour=(0, 0, 0))
        # pygame.draw.polygon(screen, (250, 0, 0), [(10, 10), (100, 10), (200, 200)])

