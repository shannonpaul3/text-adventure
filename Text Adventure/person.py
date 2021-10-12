import csv

class Person:
    with open("data/events.csv", newline='') as a:
        reader = csv.reader(a)
        events = list(reader)
        # ["Name", "Location", "Before Action", "After Action"]

    def __init__(self, name, location, items):
        self.name = name
        self.location = location
        self.items = items
        self.events = Person.events
        self.wearing = None
                
    def set_location(self, loc):
        self.location = loc
    
    def remove_item(self, item):
        for i in self.items:
            if i.name == item.name:
                self.items.remove(i)
        for a in self.events:
                if a[0] == self.name and int(a[1]) == self.location:
                    print("\n" + a[3])
    
    def add_item(self, item):
        self.items.append(item)
    
    def wear(self, item):
        self.wearing = item
        print(self.name + " is now wearing " + item.name + ".")
        if item.permanent == True:
            print("This " + item.name + "will stay on " + self.name + ".")
    
    def get_wearing(self):
        if self.wearing != None:
            print(self.name + " is wearing " + self.wearing)
    
    def check_name(self, name):
        if name == self.name.lower():
            return self
        return None