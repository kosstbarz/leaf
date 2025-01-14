from leaf.tiles import base


class Source(base.Base):
    color = (100, 150, 100)
    produce_food = 100

    def get_penetration(self, ferment_id, direction) -> float:
        return 1

    def limit(self, ferment_id) -> int:
        return 100
