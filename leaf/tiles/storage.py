import enum

from leaf.tiles import base

FOOD_FOR_BUTTON = 10


class StorageMode(enum.Enum):
    ACCUMULATE = 0
    STORE = 1
    GIVE = 2


class Storage(base.Base):
    color = (100, 100, 20)
    start_rot = 10000
    produce_food = -2

    def __init__(self):
        super().__init__()
        self.mode = StorageMode.ACCUMULATE

    def get_penetration(self, ferment_id, direction) -> float:
        if ferment_id == 0 and self.mode == StorageMode.STORE:
            return 0.001
        return 1.

    def limit(self, ferment_id) -> int:
        return 100

    def add_ferment(self, tile, ferment_id, amount):
        tile.ferments[ferment_id] += amount
        tile.visible_ferments = tile.ferments.copy()
        if self.mode == StorageMode.ACCUMULATE:
            tile.visible_ferments[0] = 0.

    def needed_buttons(self) -> list[str]:
        needed_buttons = [mode.name for mode in StorageMode if
                          self.mode != mode]
        return needed_buttons

    def button_clicked(self, tile, button):
        self.mode = StorageMode[button]
        self.add_ferment(tile, 0, -FOOD_FOR_BUTTON)
