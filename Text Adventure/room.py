from item import Item
from helper_functions import csv_loader

# Room Object
class Room:
    room_data = {}
    for r in csv_loader("data/rooms.csv"):
        room_data[r[0]] = {"description": r[1], "look": r[2], "N": r[3], "S": r[4], "E": r[5], "W": r[6], "spot": r[7]}
    
    def __init__(self, name, id, items, furniture, people):
        self.id = id
        self.name = name            #String
        self.description = Room.room_data[name]["description"]      #String: describes the room
        self.look = Room.room_data[name]["look"]
        self.people = people
        # Surrounding Rooms and Descriptions organized [N, S, E, W]
        self.surr_rooms = None
        self.surr_descriptions = [Room.room_data[name]["N"], Room.room_data[name]["S"], Room.room_data[name]["E"], Room.room_data[name]["W"]]
        self.items = items          #list<Item>: list of items found in room
        self.furniture = furniture
        self.item_spot = Room.room_data[name]["spot"]
    
    # Print room description; surroudings and objects in room
    def describe(self):
        print(self.description)

        self.dir()
    
    def look_around(self):
        index = 0

        print(self.look)

        for i in self.items:
            print("\nThere is a " + i.name + self.item_spot, end="")
            index += 1
        if len(self.items) != 0:
            print()
    
    def dir(self):
        print()
        for s in range(len(self.surr_rooms)):
            if self.surr_rooms[s] != None:
                print(self.surr_descriptions[s], end = "")
        print()
    
    def add_item(self, item):
        self.items.append(item)
    
    def remove_item(self, item):
        for i in self.items:
            if i == item:
                self.items.remove(i)
    
    def remove_person(self, person):
        for p in self.people:
            if p.name == person:
                self.people.remove(p)

    def add_person(self, person, characters):
        for p in characters:
            if p.name == person:
                self.people.append(p)
    
    def get_person(self, person):
        for p in self.people:
            if p.name == person:
                return p
    
    def set_surr(self, list):
        self.surr_rooms = list

    def open_room(self, room, direction, rooms):
        for r in rooms:
            if r.name == room:
                self.surr_rooms[direction] = r

        