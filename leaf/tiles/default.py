
class Default:
    color = (100, 100, 100)

    def update(self, tile):
        if tile.owner is not None:
            tile.food -= 1

    def get_penetration(self, direction) -> float:
        return 0.5

    def limit(self) -> int:
        return 20
