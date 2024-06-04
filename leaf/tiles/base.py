
class Base:
    produce_food = 0
    start_rot = 1000
    rot_max = 100
    start_rot_min = 10

    def __init__(self):
        self.is_rottening = False

    def update(self, tile):
        tile.ferments[0] += self.produce_food
        if tile.ferments[0] > self.start_rot:
            tile.add_ferments(1, int((tile.ferments[0] - self.start_rot) / 10))
            self.is_rottening = True
        elif tile.ferments[0] < self.start_rot_min:
            tile.add_ferments(1, self.start_rot_min - tile.ferments[0])
            self.is_rottening = True
        else:
            self.is_rottening = False
        tile.visible_ferments = tile.ferments.copy()

    def add_ferment(self, tile, ferment_id, amount):
        tile.ferments[ferment_id] = max(tile.ferments[ferment_id] + amount, 0)
        tile.visible_ferments = tile.ferments.copy()

    def needed_buttons(self) -> list[str]:
        return []
