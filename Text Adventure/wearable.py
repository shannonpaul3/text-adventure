# inherit Item
from item import Item

class Wearable(Item):
    def __init__(self, name, uses, permanent, for_player):
        super().__init__(name, uses)
        self.worn_by = None
        self.permanent = permanent
        self.for_player = for_player
