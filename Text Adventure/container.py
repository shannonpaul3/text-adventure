# inherit Portable
from portable import Portable


class Container(Portable):
    def __init__(self, name, uses, full, liquid):
        Portable.__init__(self, name, uses)
        self.full = full
        self.liquid = liquid
        self.lit = False
        self.full_description = self.get_description(self.description)

    def get_description(self, description):
        # print("in description", self.full)
        output = self.description
        if self.full:
            output = output + " The " + self.name + " is full of " + self.liquid + "."
        else:
            output = output + " The " + self.name + " is empty."
        if self.lit:
            output = output + " The " + self.name + " is on." 
        return output
    
    def set_full(self, f, l):
        self.full = f
        self.liquid = l
    
    def set_lit(self, l):
        self.lit = True