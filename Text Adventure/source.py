# Shannon Paul
# 101178140

from item import Item
from portable import Portable
from container import Container
from wearable import Wearable
from furniture import Furniture
from room import Room
from person import Person

import sys


################# Functions ##########################

def initialize(game_data):
    game_data["game_over"] = False

    # Initialize Portable Items (name, uses)
    # flask = Container("flask", ["drink", "fill"], True, "liquor")

    hat = Wearable("hat", ["wear"], False, True)
    note = Portable("note", ["read"])
    needle = Portable("needle", ["use", "stitch"])
    silk = Portable("silk", ["use"])
    cotton = Portable("cotton", ["apply"])
    gauze = Portable("gauze", ["apply"])
    bed = Furniture("bed", ["lay on"])
    lighter = Portable("lighter", ["light"])
    lantern = Container("lantern", ["light"],False, None)
    fuel = Portable("fuel", [])
    letter = Portable("letter", [])
    bandana = Portable("bandana", [])
    pistol = Portable("pistol", [])
    gold = Portable("gold", [])

    # Set pairs (items that must be used together)


    # Initialze People (name, location, items)
    jet = Person("Jet", 1, [note, letter])
    beau = Person("Beau", 5, [])
    milly = Person("Milly", 5, [])
    sheriff = Person("Sheriff", 10, [])

    # Initialize Rooms (name, id, items, people)
    cottage = Room("Cottage", 0, [needle, silk, cotton, gauze], [bed], [])
    front_yard = Room("Front Yard", 1, [], [], [jet])
    east_shore = Room("East Shore", 2, [], [], [])
    west_shore = Room("West Shore", 3, [lantern], [], [])
    bay = Room("Bay", 4, [], [], [])
    beaus_barn = Room("Beau's Barn", 5, [], [], [beau, milly])
    beaus_yard = Room("Beau's Backyard", 6, [], [], [])
    beaus_house = Room("Beau's House", 7, [], [bed], [])
    well = Room("Well", 8, [fuel], [], [])
    main_intersection = Room("Main Intersection", 9, [], [], [])
    sheriffs_house = Room("Sheriff's House", 10, [], [], [sheriff])
    waterfall = Room("Waterfall", 11, [], [], [])
    long_tunnel = Room("Long Tunnel", 12, [], [], [])
    intersection = Room("Intersection", 13, [], [], [])
    dead_end = Room("Dead End", 14, [gold], [], [])
    bandit_hq = Room("Bandit HQ", 15, [], [], [])
    dam = Room("Dam", 16, [], [], [])

    #Set-up surrounding rooms
    cottage.set_surr([None,front_yard,None,None])
    front_yard.set_surr([cottage,main_intersection,None,east_shore])
    east_shore.set_surr([None,bay,front_yard,west_shore])
    west_shore.set_surr([None,bay,east_shore,None])
    bay.set_surr([east_shore,None,None,beaus_barn])
    beaus_barn.set_surr([None,beaus_yard,bay,None])
    beaus_yard.set_surr([beaus_barn, beaus_house,None,None])
    beaus_house.set_surr([beaus_yard,None,main_intersection,well])
    well.set_surr([beaus_house,None,None,None])
    main_intersection.set_surr([front_yard,None,None,beaus_house])
    sheriffs_house.set_surr([main_intersection,None,None,None])
    waterfall.set_surr([long_tunnel, east_shore, None, None])
    long_tunnel.set_surr([intersection, waterfall, None, None])
    intersection.set_surr([bandit_hq,long_tunnel,None,dead_end])
    bandit_hq.set_surr([None,intersection,dam,None])
    dead_end.set_surr([None,None,intersection,None])
    dam.set_surr([None,bandit_hq,None,None])

    # Master Lists
    game_data["rooms"] = [cottage, front_yard, east_shore, west_shore, bay, beaus_barn, beaus_yard, beaus_house, well, main_intersection, sheriffs_house, waterfall, long_tunnel, intersection, bandit_hq, dead_end, dam]
    game_data["items"] = [note, needle, silk, cotton, gauze, bed, lighter, lantern, fuel, letter, hat, bandana, pistol, gold]
    game_data["characters"] = [jet, beau, milly, sheriff]

    # events
    game_data["events"] = {
        "note_delivered": False,
        "meet_milly": False,
        "carry_beau": False,
        "treat_beau": False,
        "letter_delivered": False,
        "meet_sheriff": False,
        "destroyed_dam": False
        }

    # Player starts with empty inventory and carrying no one
    game_data["inventory"] = []
    # Current location and turn
    game_data["curr_location"] = 0
    game_data["turn"] = 1
    game_data["score"] = 0

# Describe current curr_location
def give_description(game_data):
    game_data["rooms"][game_data["curr_location"]].describe()

# Display current score
def show_data(game_data):
    print()
    print("Turn: ", game_data["turn"], " ---- " + game_data["rooms"][game_data["curr_location"]].name + " ---- ")
    print()

################# Handlers ##########################

def handle_input(game_data):

    while(1):
        print("\nWhat would you like to do?")
        phrase = input(">> ").lower().strip().split()
        
        if find("help", phrase) or find("hint", phrase):
            need_help()
        if find("look", phrase):
            print()
            game_data["rooms"][game_data["curr_location"]].describe()
            print()
            game_data["rooms"][game_data["curr_location"]].look_around()
            check_location(None, game_data)
            check_events(game_data)
        if find("directions", phrase) or find("d", phrase):
            game_data["rooms"][game_data["curr_location"]].dir()
        
        # Handle Character Interactions
        handle_interactions(phrase, game_data)

        # Handle Items and Inventory
        handle_items(phrase, game_data)

        # Handle Directions (returns true if room changes)
        if handle_directions(phrase, game_data):
            break

        if find("quit", phrase) or find("q", phrase):
            print("Are you sure you want to quit?")
            phrase = input(">> ").lower().strip().split()
            if find("yes", phrase):
                game_data["game_over"] = True
                sys.exit
                break

def handle_items(phrase, game_data):
    
    if (find("take", phrase) and find("all", phrase)):
        for i in game_data["rooms"][game_data["curr_location"]].items:
            i.found = True
            game_data["inventory"].append(i)
        game_data["rooms"][game_data["curr_location"]].items = []
        print("\nAll the items from the " + game_data["rooms"][game_data["curr_location"]].name + " have been added to your inventory. (HINT: type 'i' to see your inventory)")
    elif find("take", phrase) or (find("pick", phrase) and find("up", phrase)) or find("get", phrase) or find("carry", phrase):
        item = find_item(phrase, game_data)
        person = find_person(phrase, game_data)
        if item == "not found":
            print("\nCannot take that.")
        elif person != "not found":
            print("Carrying " + person.name)
        else:
            if in_place(item, game_data["inventory"]):
                print("\nYou already have that item.")
            else:
                person = person_has(item, game_data)
                if person != None:
                    item.found = True
                    game_data["inventory"].append(item)
                    print("\nYou took the " + item.name + " from " + person.name + ". It has been added to your inventory.")
                    person.remove_item(item)
                elif in_place(item, game_data["rooms"][game_data["curr_location"]].items):
                    item.found = True
                    game_data["inventory"].append(item)
                    print("\n" + item.name + " has been added to your inventory. (type 'i' or 'inventory' to see your inventory)")
                    game_data["rooms"][game_data["curr_location"]].remove_item(item)
                else:
                    print("\nThat item is not here.")
    
    if (find("put", phrase) and find("on", phrase)):
        item = find_item(phrase, game_data)
        person = find_person(phrase, game_data)
        if item != "not found" and person != "not found":
            if game_data["events"]["carry_beau"] == True and item.name == "bed" and in_place(item, game_data["rooms"][game_data["curr_location"]].furniture) and person.name == "Beau":
                game_data["events"]["carry_beau"] = None
                check_events(game_data)
            else:
                print("Try something else.")
        else:
            print("Can't find those.")
            
    if find("drop", phrase) or find("leave", phrase) or (find("put", phrase) and find("down", phrase)):
        item = find_item(phrase, game_data)
        if item == "not found":
            print("\nNot in inventory.")
        else:
            if game_data["events"]["carry_beau"] == True:
                if item.name == "needle" or item.name == "silk" or item.name == "cotton" or item.name == "gauze":
                    print("\nYou will need that to treat Beau's wounds. Hold on to it.")
            elif in_place(item, game_data["inventory"]):
                game_data["inventory"].remove(item)
                print("\nYou dropped the " + item.name)
                game_data["rooms"][game_data["curr_location"]].add_item(item)
            else:
                print("\nYou're not carrying that item.")

    if find("inspect", phrase) or find("examine", phrase) or find("x", phrase) or find("read", phrase):
        item = find_item(phrase, game_data)
        if item == "not found":
            print("\nDon't see that item anywhere.")
        else:
            if in_place(item, game_data["inventory"]):
                item.found = True
                if isinstance(item, Container):
                    print("\n" + item.full_description)
                else:
                    print("\n" + item.description)
            else:
                print("\nYou must pick up the item to inspect it.")
    
    if find("light", phrase):
        item = find_item(phrase, game_data)
        if item != "not found":
            if item.name == "lantern":
                if in_place(item, game_data["inventory"]):
                    if item.full == False:
                        print("\nThe lantern must be filled with fuel.") 
                    else:
                        lighter = find_item(["lighter"], game_data)
                        if in_place(lighter, game_data["inventory"]):
                            item.set_lit(True)
                            item.full_description = item.get_description(item.description)
                            print("You lit the lantern.")
                        else:
                            print("\nYou need a lighter to light the lantern.")
            else:
                print("\nYou can't light that item.")
        else:
            print("\nItem not found.")

    if find("inventory", phrase) or find("i", phrase):
        show_inventory(game_data)

    if find("drink", phrase) or find("empty", phrase):
        item = find_item(phrase, game_data)
        if in_place(item, game_data["inventory"]):
            if isinstance(item, Container):
                if item.full:
                    print("\nYou drank " + item.liquid + " from the " + item.name + ".")
                    item.set_full(False, "nothing")
                    item.full_description = item.get_description(item.description)
                else:
                    print("\nThe " + item.name + " is empty.")
            else:
                print("\nThat item is not a container.")
        else:
            print("\nYou aren't carrying that item.")
    
    if find("fill", phrase):
        item = find_item(phrase, game_data)
        if item != "not found":
            if item.name == "lantern":
                if in_place(item, game_data["inventory"]):
                    if item.full:
                        print("\nThe lantern is already full of fuel.") 
                    else:
                        fuel = find_item(["fuel"], game_data)
                        if in_place(fuel, game_data["inventory"]):
                            item.set_full(True, "fuel")
                            item.full_description = item.get_description(item.description)
                            print("\nYou filled the lantern with fuel.")
                        else:
                            print("\nYou need fuel in your inventory to fill the lantern.")
            else:
                print("\nYou can't fill that item.")
        else:
            print("\nItem not found.")


def handle_directions(phrase, game_data):
    
    if find("n", phrase):
        north_room = game_data["rooms"][game_data["curr_location"]].surr_rooms[0]
        if  north_room == None:
            print("\n" + game_data["rooms"][game_data["curr_location"]].surr_descriptions[0])
        else:
            if north_room.name == "Long Tunnel":
                lantern = find_item(["lantern"], game_data)
                if in_place(lantern, game_data["inventory"]) and lantern.lit == True:
                        print("\nYour lantern will light the way in the dark tunnel.")
                        change_rooms(north_room, game_data)
                        return True
                print("\nYou won't be able to see in the dark tunnel without a light source.")
            else:
                change_rooms(north_room, game_data)
                return True
    elif find("s", phrase):
        south_room = game_data["rooms"][game_data["curr_location"]].surr_rooms[1]
        if  south_room == None:
            print("\n" + game_data["rooms"][game_data["curr_location"]].surr_descriptions[1])
        else:
            change_rooms(south_room, game_data)
            return True
    elif find("e", phrase):
        east_room = game_data["rooms"][game_data["curr_location"]].surr_rooms[2]
        if  east_room == None:
            print("\n" + game_data["rooms"][game_data["curr_location"]].surr_descriptions[2])
        else:
            change_rooms(east_room, game_data)
            return True
    elif find("w", phrase):
        west_room = game_data["rooms"][game_data["curr_location"]].surr_rooms[3]
        if  west_room == None:
            print("\n" + game_data["rooms"][game_data["curr_location"]].surr_descriptions[3])
        else:
            change_rooms(west_room, game_data)
            return True
    return False

def handle_interactions(phrase, game_data):
    if find("talk", phrase):
        check_location("talk", game_data)
    elif find("ask", phrase):
        check_location("ask", game_data)

################# Update ##########################

def update(game_data):
    game_data["turn"] += 1

def meet_milly(game_data):
    
    print("\nMILLY, running over to you: Doc! I'm so glad you're here! Please help us. My dad... he doesn't look too good... Do you think you could help?")
    phrase = input(">> ").lower().strip().split()
    if find("no", phrase):
        game_data["rooms"][game_data["curr_location"]].describe()
        return
    elif find("yes", phrase):
        if check_tools(game_data):
            print("\nMILLY: I knew you would help us old friend. Come with me!", end = "")
        else:
            print("\nMILLY: I was hoping you'd bring all them doctor tools with you... I'm no doctor but I think you're gonna need em...")
            print("\nYou'll need to find all your medical tools to help out Milly and Beau.")
            game_data["rooms"][game_data["curr_location"]].describe()
            return
    else:
        if check_tools(game_data):
            print("\nMILLY: I'll take that as a yes!", end = "")
        else:
            print("\nMILLY: I was hoping you'd bring all them doctor tools with you... I'm no doctor but I think you're gonna need em...")
            print("\nYou'll need to find all your medical tools to help out Milly and Beau.")
            game_data["rooms"][game_data["curr_location"]].describe()
            return
    print("\nMilly takes you by the hand and walks you over to her father.")
    print("\nBEAU: Good to see ya Doc. Welcome back.")
    phrase = ""
    while not(find("a", phrase) or find("b", phrase) or find("c", phrase)):
        print("\nSelect a response: ")
        print("\na. What happened?")
        print("b. How are you feeling?")
        print("c. Where did those cuts come from?")
        phrase = input(">> ").lower().strip().split()
    if find("a", phrase) or find("c", phrase):
        print("\nBEAU: I'm note too sure Doc... I was hoping you could tell me.")
        print("\nSelect a response: ")
        print("\nb. How are you feeling?")
        input(">> ")
    print("\nBEAU: I was feeling alright this morning... asides from being pretty thirsty. Not sure if you've noticed but the creek has been dried up for some time now, so we've been travelling to the outskirts to fill up from other water supplies. Maybe I'm just picky... but that other water don't refresh ya quite like our fresh canyon water. I've been letting Milly finish the last bit of our personal supply cause she deserves the good stuff. Anyways, all the sudden I start getting these rashes on my body and some of em start bleeding... so right now not feeling too great. I sure am happy you're here.")
    phrase = ""
    while not(find("a", phrase) or find("b", phrase)):
        print("\nSelect a response: ")
        print("\na. Has the creek ever dried up before?")
        print("b. Let's take a look at those cuts.")
        phrase = input(">> ").lower().strip().split()
    if find("a", phrase):
        print("BEAU: Our family has been living here and transporting water from the bay for generations... not once has it been dried up. The creek has been so reliable and the water is so refreshing that the towns people consider it magical... It's a real shame but nature does as nature does.")
        print("\nSelect a response: ")
        print("b. Let's take a look at those cuts.")
        input(">> ")
    else:
        print("\nYou approach Beau and begin to inspect his cuts. He has some kind of rash all over his body - not like something you've seen or heard of before. In some spots, the rash has split open and his Beau is bleeding. Those wounds will need to be treated.")
        print("\nSelect a response: ")
        print("\na. Has the creek ever dried up before?")
        input(">> ")
        print("\nBEAU: Our family has lived here and transported water from the bay for generations... not once has it been dried up. It's been so reliable that the towns people consider it magical... It's a real shame but nature does as nature does.")
    phrase = ""
    while not(find("a", phrase) or find("b", phrase)):
        print("\nSelect an action: ")
        print("\na. Treat wounds.")
        print("b. Help Beau up.")
        phrase = input(">> ").lower().strip().split()
    if find("a", phrase):
        print("\nThere is lots of sand and dirt in here that could infect the wound. It's probably best to go somewhere with a bed for Beau to lie down.")
        print("\nSelect an action: ")
        print("\nb. Help Beau up.")
        input(">> ")
    print("Milly helps you get Beau onto his feet.")
    print("\nMILLY: I'll help you carry my dad wherever you think is best.\n")
    game_data["rooms"][game_data["curr_location"]].describe()
    game_data["events"]["carry_beau"] = True
    game_data["events"]["meet_milly"] = True

def check_tools(game_data):
    tools = 0
    for i in game_data["inventory"]:
        if i.name == "needle" or i.name == "silk" or i.name == "cotton" or i.name == "gauze":
            tools +=1
    if tools < 4:
        return False
    return True

def treat_beau(game_data):
    print("\nBeau is now in a sterile envrionment and risk of infection has decreased significantly. While being transported, some of Beau's cuts split open even more. They urgently need to be treated.")
    
    show_inventory(game_data)
    print("\nSelect an item to treat Beau:")
    phrase = input(">> ").lower().strip().split()
    while not find("gauze", phrase):
        print("\nBefore moving forward you need to stop the bleeding. Pressure must be applied to do so.")
        show_inventory(game_data)
        print("\nSelect an item to treat Beau:")
        phrase = input(">> ").lower().strip().split()
    item = find_item(["gauze"], game_data)
    print("\n" + item.description)
    game_data["inventory"].remove(item)
    print("\nYou wrap the gauze around Beau's wounds and stop the bleeding. This will allow you to further treat Beau's wounds one at a time.")
    show_inventory(game_data)
    print("\nSelect an item to treat Beau:")
    phrase = input(">> ").lower().strip().split()
    while not find("cotton", phrase):
        print("\nYou can't properly see where the cuts start and end. They need to be cleaned first.")
        show_inventory(game_data)
        print("\nSelect an item to treat Beau:")
        phrase = input(">> ").lower().strip().split()
    item = find_item(["cotton"], game_data)
    print("\n" + item.description)
    game_data["inventory"].remove(item)
    print("\nWith the sterile piece of cotton, you clean up the area around the wound you are currently trying to close. You are now able to see clearly where the cut begins and ends.")
    show_inventory(game_data)
    print("\nSelect an item to treat Beau:")
    phrase = input(">> ").lower().strip().split()
    while not find("needle", phrase):
        print("The bleeding is getting worse. The wounds need to be closed up.")
        show_inventory(game_data)
        print("\nSelect an item to treat Beau:")
        phrase = input(">> ").lower().strip().split()
    item = find_item(["needle"], game_data)
    print("\n" + item.description)
    game_data["inventory"].remove(item)
    show_inventory(game_data)
    print("\nSelect an item to treat Beau:")
    phrase = input(">> ").lower().strip().split()
    while not find("silk", phrase):
        print("You need the proper tools to suture the wounds.")
        print("\nSelect an item to treat Beau:")
        phrase = input(">> ").lower().strip().split()
    item = find_item(["silk"], game_data)
    print("\n" + item.description)
    game_data["inventory"].remove(item)
    print("\nYou sutured up Beau's wounds. He will be okay for now.")

    print("\nMILLY: Thank you so much Doctor. If you do find a permanent solution please let us know.")
    print("BEAU: Appreciate your help. Please take this as a sign of appreciation. ")
    print("\nBeau hands you a lighter. It's been added to your inventory.")
    print("\nBEAU: I found it while I was transporting water.")

    item = find_item(["lighter"], game_data)
    game_data["inventory"].append(item)
    item = find_item(["note"], game_data)
    game_data["items"].remove(item)
    
    game_data["events"]["letter_delivered"] = True
    game_data["events"]["treat_beau"] = False

def meet_sheriff(game_data):
    print("SHERIFF: Howdy... I'm glad you came. Something fishy is going on around here...")
    phrase = ""
    while not(find("a", phrase) or find("b", phrase)):
        print("\nSelect a response: ")
        print("\na. What do you mean, Sheriff?")
        print("b. I know exactly what you mean...")
        phrase = input(">> ").lower().strip().split()
    if find("a", phrase):
        print("\nSHERIFF: Well first the sacred creek runs dry and now all our people are getting rashes! I don't think it's a coincidence...", end = " ")
    else:
        print("\nSHERIFF: I knew you'd put it together Doc... It's not a coincidence the creek runs dry and our people start getting rashes...",end = " ")
    print("Now tell me Doc, where does the water in the creek come from?")
    phrase = input(">> ").lower().strip().split()
    if find("canyon", phrase):
        print("\nSHERIFF: That's right Doc!", end = " ")
    else:
        print("\nSHERIFF: ", end = "")
    print("It runs down from the canyon. I wanted to go check it out but I can't leave my people behind in this time of need... not to mention this rash really do hurt. I was hoping you could go see if there's something blocking the flow of water. Could you do that for us?")
    phrase = input(">> ").lower().strip().split()
    if find("no", phrase):
        print("\nSHERIFF: I'm not taking no for an answer. We need ya Doc!", end = " ")
    else:
        print("\nSHERIFF: I knew I could count on you!", end = " ")
    print("You know that waterfall that runs into the creek? Well it leads right to the canyon. Now of course I don't expect you to climb it... word is there's a secret tunnel through the waterfall that'll take you right to the source. Do be careful of them bandits though... sometimes they can be found in those tunnels mining for gold.")
    phrase = ""
    while not(find("a", phrase) or find("b", phrase)):
        print("\nSelect a response: ")
        print("\na. What should I do if I run into them?")
        print("b. I'm not scared of any bandits...")
        phrase = input(">> ").lower().strip().split()
    if find("a", phrase):
        print("\nSHERIFF: Well let's hope you don't... Just in case I have a few things for you.")
    if find("b", phrase):
        print("\nSHERIFF: I wish I had your bravery Doc. To make sure you're prepared, I have a few things for you.")
    print("\nThe Sheriff hands you a hat, a bandana and a pistol. they've been added to your inventory.")
    print("\nSHERIFF: Now that hat and bandana should help you blend right in. I don't think I need to explain what the pistol is for... Now go on Doc!\n")

    item = find_item(["hat"], game_data)
    game_data["inventory"].append(item)
    item = find_item(["bandana"], game_data)
    game_data["inventory"].append(item)
    item = find_item(["pistol"], game_data)
    game_data["inventory"].append(item)
    
    item = find_item(["letter"], game_data)
    game_data["items"].remove(item)
    
    game_data["rooms"][2].open_room("Waterfall", 0, game_data["rooms"])
    game_data["rooms"][game_data["curr_location"]].describe()
    game_data["events"]["meet_sheriff"] = True

################# Helper Functions ##########################

def change_rooms(room, game_data):
    for i in game_data["rooms"]:
        if i == room:
            game_data["curr_location"] = i.id

def check_location(text, game_data):

    if game_data["curr_location"] == 5 and game_data["events"]["meet_milly"] == False:
        if text == "talk" or text == "ask":
            meet_milly(game_data)
        else:
            print("Sitting against the wall is Beau. He looks as though he is in mountains of pain.", end = " ")
            print("By his side, his daughter Milly looks very concerned.")
            print("\nHINT: you can talk to other characters")
    
    if game_data["curr_location"] == 10 and game_data["events"]["meet_sheriff"] == False:
        if text == "talk" or text == "ask":
            meet_sheriff(game_data)
        else:
            print("Sitting at her desk, shining her badge, is the town's Sheriff.", end = " ")
    
    if game_data["curr_location"] == 16:
        phrase = ""
        while not(find("yes", phrase)):
            print("Would you like to destroy the dam?")
            phrase = input(">> ").lower().strip().split()
        print("\nYou destroyed the dam and the water flowed back into the creek. Looks like the rumours were true... In this town the water protects the town's people from a fungal virus in the sand. Good work Doc!")
        game_data["game_over"] = True
        game_data["events"]["destroyed_dam"] = True
        sys.exit
        

# Check what event should be happening
def check_events(game_data):
    
    if game_data["events"]["note_delivered"] == False:
        for i in game_data["items"]:
            if i.name == "note" and i.found == True:
                game_data["rooms"][game_data["curr_location"]].remove_person("Jet")
                game_data["events"]["note_delivered"] = True
        if game_data["curr_location"] == 0:
            for i in game_data["items"]:
                if i.name == "note" and i.found != True:
                    print("\nYou can hear a hawk screeching outside.")
        if game_data["curr_location"] == 1:
            for p in game_data["rooms"][game_data["curr_location"]].people:
                for a in p.events:
                    if a[0] == p.name and int(a[1]) == game_data["curr_location"]:
                        print("\n" + a[2])
                        break
    
    if game_data["events"]["carry_beau"] == True:
        print("\nMilly is standing next to you helping support Beau's weight.")
        game_data["events"]["note_delivered"] = True
        item = find_item(["note"], game_data)
        if in_place(item, game_data["inventory"]):
            game_data["inventory"].remove(item)
    if game_data["events"]["carry_beau"] == None:
        print("\nMilly helps you lay Beau down on the bed. Beau is now more comfortable.")
        game_data["events"]["carry_beau"] = False
        game_data["events"]["treat_beau"] = True
    
    if game_data["events"]["treat_beau"] == True:
        treat_beau(game_data)
    
    if game_data["events"]["letter_delivered"] == True:
        for i in game_data["items"]:
            if i.name == "letter" and i.found == True:
                game_data["rooms"][game_data["curr_location"]].remove_person("Jet")
                game_data["events"]["letter_delivered"] = False
                game_data["rooms"][9].open_room("Sheriff's House", 1, game_data["rooms"])
    if game_data["events"]["letter_delivered"] == True:
        if game_data["curr_location"] == 0 or game_data["curr_location"] == 7:
            for i in game_data["items"]:
                if i.name == "letter" and i.found != True:
                    print("\nYou can hear a hawk screeching in the yard.")
                    if game_data["curr_location"] == 0:
                        game_data["rooms"][1].add_person("Jet", game_data["characters"])
                    elif game_data["curr_location"] == 7:
                        game_data["rooms"][6].add_person("Jet", game_data["characters"])
        if game_data["curr_location"] == 1 or game_data["curr_location"] == 6:
            for p in game_data["rooms"][game_data["curr_location"]].people:
                for a in p.events:
                    if a[0] == p.name and int(a[1]) == 99:
                        print("\n" + a[2])
                        break
                break


# Returns True if word found in phrase
def find(word, phrase):
    for w in phrase:
        if w == word:
            return True
    return False

# look for item's mentioned by user
def find_item(phrase, game_data):
    found_item = "not found"
    for i in phrase:
        for j in game_data["items"]:
            if i == j.name:
                found_item  = j
    return found_item

# look for person mentioned by user
def find_person(phrase, game_data):
    for p in phrase:
        for c in game_data["characters"]:
            found = c.check_name(p)
            if found != None:
                return found
    return "not found"

def person_has(item, game_data):
    for p in game_data["rooms"][game_data["curr_location"]].people:
        if in_place(item, p.items):
            return p
    return None

# check if item in place (inventory, room, etc.)
def in_place(item, place):
    for i in place:
        if i == item:
            return True
    return False

def show_inventory(game_data):
    print("\nInventory: ", end = " ")
    for i in game_data["inventory"]:
        print(i.name, end = " ")
    print()

def need_help():
    print("\nTry entering keywords such as: ")
    print("look - to get more detail about ur surroundings")
    print("directions/d - describes what is in different directions")
    print("inspect/examine/x [item] - to inspect/examine an object")
    print("take/pick up/get [item] - to take/pick up object")
    print("leave/put down/drop [item] - to leave/drop an item")
    print("To move in a certain direction use N, S, E, or W")
    print("\nType 'quit' to quit")

def main():
    
    need_help()
    game_data = {}
    initialize(game_data)

    while not game_data["game_over"]:
        show_data(game_data)
        give_description(game_data)
        check_location(None, game_data)
        check_events(game_data)
        if(game_data["events"]["destroyed_dam"] == True):
            break
        handle_input(game_data)
        update(game_data)

if __name__ == "__main__":
    main()