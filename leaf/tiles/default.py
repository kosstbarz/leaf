from leaf.tiles import base


class Default(base.Base):
    color = (100, 100, 100)
    produce_food = -1

    def update(self, tile):
        if tile.owner is not None:
            tile.add_ferments(0, -1)
        if tile.ferments[0] > self.start_rot:
            tile.add_ferments(1, int((tile.ferments[0] - self.start_rot) / 10))
            self.is_rottening = True
        elif tile.ferments[0] < self.start_rot_min:
            tile.add_ferments(1, self.start_rot_min - tile.ferments[0])
            self.is_rottening = True
        else:
            tile.add_ferments(1, -1)
            self.is_rottening = False
        tile.visible_ferments = tile.ferments.copy()

    def get_penetration(self, ferment_id, direction) -> float:
        return 0.5

    def limit(self, ferment_id) -> int:
        return 20
