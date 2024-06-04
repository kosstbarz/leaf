import enum
from typing import Optional

neighbour_ids_even = [
    (-1, -1),
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 1),
    (-1, 0)
]
neighbour_ids_odd = [
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 0)
]


class Dir(enum.Enum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    RIGHT = 2
    DOWN_RIGHT = 3
    DOWN_LEFT = 4
    LEFT = 5

    def opposite(self):
        return Dir((self.value + 3) % 6)


def get_index(idx, idy, direction_: Dir):
    if isinstance(direction_, int):
        direction_ = Dir(direction_)
    if idy % 2 == 0:
        diff = neighbour_ids_even[direction_.value]
    else:
        diff = neighbour_ids_odd[direction_.value]
    return idx + diff[0], idy + diff[1]


def get_direction(tile1, tile2) -> Optional[Dir]:
    x_diff = tile2.position[0] - tile1.position[0]
    y_diff = tile2.position[1] - tile1.position[1]
    neightbor_list = neighbour_ids_even if tile1.position[1] % 2 == 0 else neighbour_ids_odd
    if (x_diff, y_diff) not in neightbor_list:
        return None
    return Dir(neightbor_list.index((x_diff, y_diff)))
