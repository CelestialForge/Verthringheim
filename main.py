# IT140 - Text Game - Brian Larson
# Program requirements
# >=8 Rooms
# >=6 Items - 1 item per room
# 1 Villain Room - No Items
# 1 Player Start Room - No Items
# NEWS Travel style

# Imports area
import RoomInfo
import CharacterInfo
import ItemInfo
import time
import os
import sys


# Print at specified location, for overwriting lines
def print_at(row, col, text):
    # \x1b[%d;%df - Move cursor to position %d; %d
    # \x1b[2K - clear line
    # %s - print string
    print("\x1b[%d;%df\x1b[2K%s" % (row, col, text + "\n"))


# Print Game Title
def title():
    width = 70
    game_name = "Adventure at Castle Verthringheim"
    buffer_width = int((width - len(game_name) - 2) / 2)
    print("╔" + "═" * (width - 2) + "╗")
    print("║" + (" " * buffer_width) + game_name + (" " * (width - len(game_name) - buffer_width - 2)) + "║")
    print("╚" + "═" * (width - 2) + "╝")


# Welcome text and player name entry
def introduction():
    print("Welcome to Castle Verthringheim. You are on a quest to subdue the \n" +
          "mad sorcerer Balzaquat. You are an adventurer. You've got this.")
    print()
    print("You awaken slowly, groggily. You take a moment to steady yourself.")
    p_name = input("Can you remember your name(Enter your name)? ")
    if p_name.lower() == "balzaquat":
        print("Nice try. That's is who you are here to confront, \'Hero\'.")
        p_name = "\'Hero\'"
    elif p_name != "" \
            and p_name is not None \
            and p_name.lower() != "n" \
            and p_name.lower() != "no" \
            and p_name.lower() != "yes" \
            and p_name.lower() != "y":
        print("Good.", end=" ")
        p_name = p_name.capitalize()
    else:
        print("That's ok.", end=" ")
        p_name = "Player"
    print("In case that fall was worse than you thought,")
    print("type \"HELP\" to check your guide for a refresher.")
    print("Type \'QUIT\' to end the game.")
    print()
    input("Press <Enter> when you are ready to open your eyes.")  # pause until ready.
    return p_name


# Help Guide
def show_help():
    print("Adventurer's Guide to Adventuring!")
    print("Requirements: Before facing your foe, you must have (and wear) a sword, a shield, armor, a helm,")
    print("boots and a protective amulet. If you do not, you will surely perish.")
    print("<<< KEYWORDS >>>")
    print("Directions: NORTH, EAST, WEST, SOUTH, N, E, W, S")
    print("Move: GO or TRAVEL [direction]")
    print("Observe: LOOK [Direction, At Self, AT/IN/UNDER + item id or name]")
    print("Acquire: GET [item id or name], GET [item id or name] FROM [item id or name]")
    print("Reveal: MOVE [item id or name] to reveal items under containers")
    print("Equip: EQUIP, WEAR, or USE [item id or name]")
    print("Set Refresh Delay: WAIT [integer]")
    if debug:
        print("Turn Auto-Equip on/Off: AUTOEQ or AUTOEQUIP")
        print("Show settings: SETTINGS or OPTIONS or FLAGS")
    input("Press <Enter> to continue.")


# is string a valid direction?
def is_direction(p_string):
    return p_string == "n" or p_string == "north" or \
        p_string == "e" or p_string == "east" or \
        p_string == "w" or p_string == "west" or \
        p_string == "s" or p_string == "south"


# create graphical health display for the character
def hp_bar(character):
    bar_length = 30
    cur_hp = int((bar_length * character.get_health()) / character.get_max_health())
    if character.is_alive() and cur_hp == 0:
        cur_hp = 1
    max_hp = bar_length

    return (character.get_name() + (" " * int(15 - len(character.get_name()))) + "[" + ("■" * cur_hp) +
            (" " * (max_hp - cur_hp)) + "] " + str(character.get_health()) + "/" + str(character.get_max_health()))


# Combat system
def battle(p_party_one, p_party_two):
    input("PREPARE FOR BATTLE! (Press <Enter> when ready. He has nothing better to do, he will wait.)")
    # Battle Loop
    counter = 0
    while p_party_one.is_alive() and p_party_two.is_alive():
        counter += 1
        # Refresh screen
        os.system("cls")
        # Battle Message
        print(p_party_one.get_name(), 'initiates battle with', p_party_two.get_name())
        print("Turn:", counter)
        # Print Health Stats/HP Bar
        print(hp_bar(p_party_two))
        print(hp_bar(p_party_one))
        time.sleep(1)
        # Wait then process Party 1's attack
        msg1 = p_party_one.attack(p_party_two)
        # Update HP Bar and Hit message
        print_at(3, 0, hp_bar(p_party_two))
        print_at(5, 0, msg1)
        if not p_party_two.is_alive():
            break
        time.sleep(1)
        # Wait then Process Party 2's attack
        msg2 = p_party_two.attack(p_party_one)
        # Update HP Bar and Hit message
        print_at(4, 0, hp_bar(p_party_one))
        print_at(6, 0, msg2)
        if not p_party_one.is_alive():
            break
        time.sleep(2)

    # Outcome message
    if p_party_one.is_alive():
        print(p_party_one.get_name(), "defeated", p_party_two.get_name() + ".")
    else:
        print(p_party_two.get_name(), "defeated", p_party_one.get_name() + ".")


# Search given container/room for item and return itemID
def find_item_id_by_name(p_itemname, p_source=None):
    for i in range(len(p_source if p_source is not None else Items)):
        if str.find(Items[p_source[i] if p_source is not None else i].getname().lower(), p_itemname.lower()) != -1:
            return p_source[i] if p_source is not None else i
    return -1


# Global Variables
debug = bool(sys.argv[1]) if len(sys.argv) > 1 else False

# Main procedure
if __name__ == '__main__':
    # Setup
    waitLength = 1
    Victory = False
    Items = ItemInfo.List
    Rooms = RoomInfo.List
    Villain = CharacterInfo.VillainInfo(
        "Balzaquat", "Throne Room",
        "The Mad Sorcerer Balzaquat sits atop your king's throne, a leg draped \n" +
        "over its arm while picking his nose with his pinky finger. \n" +
        "He glances at you and goes about his business.")
    print()

    # Title
    title()
    print()

    # Intro and setup player
    player_name = introduction()
    Player = CharacterInfo.PlayerInfo(player_name)

    # Debug equipment for testing
    if debug:
        Player.get(19)  # Map

    # Begin game loop
    while True:
        # Refresh screen
        os.system("cls")

        # Show current location
        # Room Name
        print(("["+str(Rooms[Player.get_location()]["id"])+"] " if debug else "")+Player.get_location())
        # Room description
        print(Rooms[Player.get_location()]["view"])
        # Room contents
        if "items" in Rooms[Player.get_location()]:
            print("Contents:")
            for item in range(len(Rooms[Player.get_location()]["items"])):
                print("  " + ItemInfo.List[Rooms[Player.get_location()]["items"][item]].getname())
        # Room Exits
        print("Exits:" +
              ("N " if "n" in Rooms[Player.get_location()] else "") +
              ("E " if "e" in Rooms[Player.get_location()] else "") +
              ("W " if "w" in Rooms[Player.get_location()] else "") +
              ("S " if "s" in Rooms[Player.get_location()] else ""))

        # Update Map
        Items[find_item_id_by_name("Map")].update_map(Player.get_location())
        # If Player find villain
        if Villain.get_location() == Player.get_location():
            print(Villain.look_at())
            time.sleep(waitLength * 3)
            print()
            print("It dawns on " + Villain.get_name() + " why you are here and he jumps up in surprised anger.")
            print("\'You are not the first to try and take my castle! You will fail like the rest!\'")
            print("He recalls what he got caught doing and flicks residue from his pinky.")
            battle(Villain, Player)
            if not Villain.is_alive():
                print("You Win. The castle is yours!")
                break
            elif not Player.is_alive():
                print("You Lose. You fade away....")
                break
        # Prompt for action
        command = input("What will you do?:")
        # Standardize case
        command = command.lower()
        if debug:
            print("Debug: Command received: |" + (command if command != "" else "NULL") + "|")
        print()  # New line for readability

        # Parse input
        param = command.split()
        # Command Handling
        # No Entry
        if len(param) == 0:
            print("I did not catch that.")
        # [QUIT] - Exit Case
        elif param[0] == "quit":
            print("Thank you for visiting. Come back soon.")
            break
        # [HELP] - Help text / Instructions
        elif param[0] == "help":
            show_help()
        # [DEBUG] - Toggle debug mode extra characters added to obscure the command
        elif param[0] == "x1debug":
            debug = not debug
            print("Debug mode set to", debug)
        # [LOAD] + [1, 2, 3] - Debug Tool: Grant gear to player
        elif debug and param[0] == "load":
            if param[1].isnumeric() and 1 <= int(param[1]) <= 3:
                loadout = int(param[1])
                Player.get(0 + (loadout - 1) * 6)
                Player.get(1 + int(loadout / 2) * 6)
                Player.get(2 + int(loadout / 2) * 6)
                Player.get(3 + int(loadout / 2) * 6)
                Player.get(4 + int(loadout / 2) * 6)
                Player.get(5 + int(loadout / 2) * 6)
            else:
                print("DEBUG:LOADOUT: Please enter a number, 1-3")
        # [TRAVEL, GO] + [N, E, W, S , NORTH EAST, WEST, SOUTH] - Move player
        elif param[0] == "go" or param[0] == "travel" or is_direction(param[0]):
            # if parameter 0 is the direction, use it, otherwise parameter 1
            Player.move_dir(param[0] if is_direction(param[0]) else param[1])
        # [LOOK] + [AT, IN, UNDER, INSIDE, UNDERNEATH, Direction] + [ItemID, ItemName, SELF] - Examine something
        # Consider ways to clean this up
        elif param[0] == "look" or param[0] == "l":
            wait = False
            # Confirm additional parameters
            if len(param) > 1:
                # Convert "look self/#" to "look AT self/#"
                if len(param) == 2 and \
                        (param[1] == "self" or
                         (param[1].isnumeric() and 0 <= int(param[1]) < len(ItemInfo.List)) or
                         find_item_id_by_name(param[1], Rooms[Player.get_location()].get("items", None)) != -1 or
                         Player.find_item_by_name(param[1]) != -1):
                    if len(param) >= 3:
                        param[2] = param[1]
                    else:
                        param.append(param[1])
                    param[1] = "at"
                # Preposition used
                if param[1] == "at" or param[1] == "in" or param[1] == "inside" or param[1] == "i" or \
                        param[1] == "under" or param[1] == "underneath" or param[1] == "u" or param[1] == "debug" or \
                        param[1] == "d":
                    # Look target included
                    if len(param) > 2:
                        # Look Self
                        if param[2] == "self":
                            wait = True
                            Player.print()
                        # look item
                        else:
                            # Get Item ID
                            if param[2].isnumeric() and 0 <= int(param[2]) < len(ItemInfo.List):
                                item_id = int(param[2])
                            elif Player.find_item_by_name(param[2]) != -1:
                                item_id = Player.find_item_by_name(param[2])
                            else:
                                item_id = find_item_id_by_name(param[2], Rooms[Player.get_location()]['items'])
                            # Examine Item
                            if Player.has_item(item_id) or \
                                    item_id in Rooms[Player.get_location()].get("items", None):
                                wait = True
                                # How to examine the item
                                if param[1] == "at":
                                    ItemInfo.List[item_id].look_at()
                                elif param[1] == "in" or param[1] == "inside" or param[1] == "i":
                                    ItemInfo.List[item_id].look_in()
                                elif param[1] == "under" or param[1] == "underneath" or param[1] == "u":
                                    ItemInfo.List[item_id].look_under()
                                elif (param[1] == "debug" or param[1] == "d") and debug:
                                    ItemInfo.List[item_id].print_item()
                            else:
                                print("You do not see", param[2], "here.")

                    else:
                        # Look target is empty
                        print("Look", param[1], "what?")
                elif is_direction(param[1]):
                    # look direction
                    destination = Rooms[Player.get_location()].get_exit(param[1])
                    if destination != -1:
                        wait = True
                        print("You see a path leading",
                              RoomInfo.exit_words[str.find(RoomInfo.exit_format.lower(), param[1][0])],  # direction
                              "towards the",
                              Rooms[destination].m_Name + ".")  # Room Name
                    else:
                        print("You see nothing in that direction.")
                else:
                    print("You do not see", param[1], "here.")
            else:
                # Look with no parameters
                print("Look at what?")
            if wait:
                input("Press <Enter> to continue.")  # pause until ready if there is something to read.
        # [GET, TAKE] + [ItemId, ItemName] + {opt[FROM] + [ItemId, ItemName]} - Get Items
        elif param[0] == "get" or param[0] == "take":
            # Parameter 1 is empty
            if len(param) <= 1:
                print("Get what?")
            else:
                item_id = -1
                # if Parameter 1 is integer
                if param[1].isnumeric() and 0 <= int(param[1]) < len(ItemInfo.List):
                    item_id = int(param[1])
                # Get Item from container
                if len(param) >= 4 and param[2] == "from":
                    source_id = -1
                    # Get container ID if it exists
                    if param[3].isnumeric() and 0 <= int(param[3]) < len(ItemInfo.List):
                        source_id = int(param[3])
                    # Parameter 3 is a name/partial name
                    else:
                        source_id = find_item_id_by_name(param[3], Rooms[Player.get_location()]['items'])
                    # Get ID from name from contents list
                    if not param[1].isnumeric():
                        item_id = find_item_id_by_name(param[1], Items[source_id].m_Contents)
                    # source container does not exist or is not present
                    if source_id == -1 or source_id not in Rooms[Player.get_location()].get("items", None):
                        print("You do not see", param[3], "here.")
                    else:
                        # item exists in container
                        if Items[source_id].has_item(item_id):
                            print("You have taken",
                                  Items[item_id].getname(),
                                  "from the",
                                  Items[source_id].getname() + ".")
                            Player.get(item_id, Items[source_id])

                        # Item does not exist in container
                        else:
                            print("You do not see that in the", Items[source_id].getname() + ".")
                # Get Item from room
                else:
                    # Get ID from name from contents list
                    if not param[1].isnumeric():
                        item_id = find_item_id_by_name(param[1], Rooms[Player.get_location()]['items'])\
                            if 'items' in Rooms[Player.get_location()] else -1
                    # Item is not present in the room
                    if item_id not in Rooms[Player.get_location()].get('items', None):
                        print("You do not see that item here.")
                    # Item is present in the room
                    else:
                        # Item cannot be carried, ie: Container
                        if Items[item_id].m_eq_slot == -1:
                            print("You cannot carry that.")
                        # Item acquired
                        else:
                            print("You have taken the", Items[item_id].getname() + ".")
                            Player.get(item_id)
                            Rooms[Player.get_location()]['items'].remove(item_id)
        # [MOVE] + [ItemId, ItemName] - Reveal hidden items
        elif param[0] == "move":
            if param[1].isnumeric() and 0 <= int(param[1]) < len(ItemInfo.List):
                item_id = int(param[1])
            else:
                item_id = find_item_id_by_name(param[1], Rooms[Player.get_location()]['items'])
            if item_id != -1:
                print("You moved the", Items[item_id].getname() + ".")
                if Items[item_id].has_hidden():
                    print("Items hidden underneath were revealed!")
                    h_items = Items[item_id].find_all()
                    if not ('items' in Rooms[Player.get_location()]):
                        Rooms[Player.get_location()]['items'] = h_items
                    else:
                        Rooms[Player.get_location()]['items'].extend(h_items)
            else:
                print("You do not see that here.")
        # [EQUIP, WEAR] + [ItemID, ItemName] - Equip gear
        elif param[0] == "equip" or param[0] == "use" or param[0] == "wear":
            # Get ItemID
            if param[1].isnumeric() and 0 <= int(param[1]) < len(ItemInfo.List):
                item_id = int(param[1])
            else:
                item_id = Player.find_item_by_name(param[1])
            Player.equip(item_id)  # equip function validates inventory inside
        # [USE] + [ItemID, ItemName] - Use Items: Map(, Books?, Potions?)
        elif param[0] == "use":
            # Get ItemID
            if param[1].isnumeric() and 0 <= int(param[1]) < len(ItemInfo.List):
                item_id = int(param[1])
            else:
                item_id = Player.find_item_by_name(param[1])
                if ItemInfo.List[item_id].can_equip():
                    # Equip if it can be worn
                    Player.equip(item_id)  # equip function validates inventory inside
                else:
                    # is Item
                    ItemInfo.List[item_id].use()
        # [WAIT] + # - Set Refresh delay
        elif param[0] == "wait" and len(param) >= 2 and param[1].isnumeric():
            waitLength = int(param[1])
            print("Refresh delay time set to", waitLength, "seconds.")
        # [AUTOEQ], [AUTOEQUIP] - enables disables auto-equip
        elif param[0] == "autoeq" or param[0] == "autoequip":
            Player.toggle_autoeq()
        # [SETTINGS], [OPTIONS], [FLAGS] - show the options/settings flags
        elif param[0] == "settings" or param[0] == "options" or param[0] == "flags":
            print("Settings:")
            if debug:
                print("Debug mode:\t\tActive")
            print("Refresh Delay:\t" + str(waitLength))
            print("Auto-Equipping:\t" + str(Player.flag_autoequip))
            print()
            input("Press <Enter> to continue.")  # pause until ready
        # Unhandled Command
        else:
            print("I don't understand that command.")
        print()
        if not debug:
            time.sleep(waitLength)
        else:
            time.sleep(1)

    input("Press <Enter> to continue.")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
'''
Could this work??? POSSIBLE
Commands = {
    "help": help(),
    "quit": quit(),
    "look": {
        "at": Look_at(object),
        "in": Look_in(),
        "under": Look_under(),
    }
    "get": {
        "": get(),
        "from": Get_from()
    }
}
key, key, var...
Commands[look][at](object}  
key, var, key, var >> [key][key](var, var)
Commands[get][from](item, container)

if cmd[0] in commands:
    if cmd[1] in Commands[cmd[0]]:
        if cmd[2] in commands[cmd[0]][cmd1]:
        .
        .
        .
        

'''
