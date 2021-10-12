# inherit Item
from item import Item

class Portable(Item):
    def __init__(self, name, uses):
        super().__init__(name, uses)
