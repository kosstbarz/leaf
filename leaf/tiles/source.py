
class Source:
    color = (20, 100, 20)

    def update(self, tile):
        tile.food += 100

    def get_penetration(self, direction) -> float:
        return 1

    def limit(self) -> int:
        return 100
