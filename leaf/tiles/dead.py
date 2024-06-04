from leaf.tiles import base


class Dead(base.Base):
    color = (10, 10, 10)

    def update(self, tile):
        pass

    def get_penetration(self, ferment_id, direction) -> float:
        return 0

    def limit(self, ferment_id) -> int:
        return 0
