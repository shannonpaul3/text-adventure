from helper_functions import csv_loader

# Item Object
class Item:
    item_data = {}
    for r in csv_loader("data/items.csv"):
        item_data[r[0]] = {"description": r[1]}

    def __init__(self, name, uses):
        self.name = name                                        #String
        self.description = Item.item_data[name]["description"]  #String: description of item and it's location
        self.pair = None
        self.uses = uses                                        #list<String>: list of keywords/uses
        self.found = False                                      #boolean: True once item has been found

    def set_pair(self, item):
        self.pair = item