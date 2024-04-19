import ItemInfo
import RoomInfo
import main


# SpellObject(dict) - Quick creation and formatting for new spells to enter in to a spellbook
def create_spell(p_name, p_msg_if_hit="%c strikes at %t.", p_damage_type="Strength", p_target_eq=-1):
    spell = {"Name": p_name, "MessageIfHit": p_msg_if_hit, "Damage": p_damage_type}
    if p_target_eq >= 0:
        spell["Target"] = p_target_eq
    return spell


class CharacterInfo:
    m_name = ""
    m_type = 0  # 0-Player, 1-NPC
    m_desc = ""
    m_location = ""
    m_base_str = 0
    m_strength = 0
    m_base_def = 0
    m_defense = 0
    m_health = 0
    m_max_health = 0
    #               W   S   A   H   L   N
    m_equipment = []
    m_hasEquipment = False
    m_inventory = []
    m_hasInventory = False
    m_SpellBook = [0, create_spell("Attack")]

    # Initialisation
    def __init__(self, p_name="A generic character", p_type=1, p_location=0, p_description=""):
        self.m_name = p_name
        self.m_type = p_type
        self.m_location = p_location
        self.m_desc = p_description
        if p_type == 0:
            self.m_hasInventory = True
            self.m_hasEquipment = True
            self.m_inventory = []
            self.m_equipment = [-1, -1, -1, -1, -1, -1]

    # void - Show self stats, equipment and inventory
    def print(self):
        print("Stats:")
        print("Health:\t", self.m_health, "/", self.m_max_health)
        print("Strength:", self.m_strength, "\t", "Defense:", self.m_defense)
        print()
        print(self.m_name, "is wearing:")
        print("Clothing -" + "\t" + " Basic Clothes")
        if self.m_hasEquipment:
            for i in range(len(self.m_equipment)):
                print(ItemInfo.eq_loc_names[i], "-\t" + ("\t" if len(ItemInfo.eq_loc_names[i]) < 6 else ""),
                      "nothing" if self.m_equipment[i] == -1 else ItemInfo.List[self.m_equipment[i]].getname())
        if self.m_hasInventory:
            print()
            print("Held in inventory:")
            if len(self.m_inventory) == 0:
                print("Nothing")
            for i in range(len(self.m_inventory)):
                print(ItemInfo.List[self.m_inventory[i]].getname())

    # Bool - Is the character alive?
    def is_alive(self):
        return self.m_health > 0

    # Bool - Can the character wear equipment?
    def has_equipment(self):
        if self.m_hasEquipment and self.m_equipment is None:
            self.m_hasEquipment = False
        return self.m_hasEquipment

    # Bool - Can the character carry inventory?
    def has_inventory(self):
        if self.m_hasInventory and self.m_inventory is None:
            self.m_hasInventory = False
        return self.m_hasInventory

    # Str - Get the Dictionary entry of the character's current location
    def get_location(self):
        return self.m_location

    # Str - return the character's name
    def get_name(self):
        return self.m_name

    # Int - return the character's current health value
    def get_health(self):
        return self.m_health

    # Int - return the character's maximum health value
    def get_max_health(self):
        return self.m_max_health

    # Str - return the character's description string
    def look_at(self):
        return self.m_desc

    # void - Set health to zero, killing the character
    def kill(self):
        self.m_health = 0

    # void - Health adjustment bypassing defense
    def adjust_hp(self, amount):
        self.m_health += amount
        if self.m_health < 0:
            self.m_health = 0

    # void - Health adjustment modified by defense
    def take_damage(self, amount):
        self.adjust_hp(-(amount - self.m_defense))

    # void - set character stats
    def set_stats(self, hp=0, strength=0, defense=0):
        self.m_health = hp
        self.m_max_health = hp
        self.m_base_str = strength
        self.m_base_def = defense
        self.update_stats()

    # var - return item if ID specified, equipment list of not
    def get_equipment(self, slot_id):
        if slot_id == -1:
            return self.m_equipment
        else:
            return self.m_equipment[slot_id]

    # void - add item to inventory
    def add_item(self, item_id):
        self.m_inventory.append(item_id)

    # void - move character to location with no checks/Teleport
    def move_to(self, p_dest_id):
        # debug function for teleportation
        self.m_location = p_dest_id

    # void - have character travel in direction, if possible
    def move_dir(self, direction):
        # For simplicity, we take the lowercase first letter only
        direction = direction[0].lower()
        # dictionary Movement
        if direction in RoomInfo.exit_words_d:  # direction is a valid cardinal direction
            if direction in RoomInfo.List[self.m_location]:  # exit is valid for this room
                # Update current room and let player know
                self.m_location = RoomInfo.List[self.m_location][direction]
                print("You travel", RoomInfo.exit_words_d[direction] + ".")
            else:  # Invalid Exit
                print("You cannot go that way.")
        else:  # Invalid direction
            print("Go where?")

    # str - conduct an attack against target, chosen from spellbook. Returns attack message and hit/miss
    def attack(self, target):
        if len(self.m_SpellBook) <= 1:
            print(self.m_name, "has no attacks/spells!")
            return
        # Decide next skill to cast. If at the end of the spellbook, cast last skill
        if self.m_SpellBook[0] < len(self.m_SpellBook) - 1:
            self.m_SpellBook[0] += 1
        # Get Spell Info for the next skill
        next_skill = self.m_SpellBook[self.m_SpellBook[0]]

        # For now, all attacks hit unless targeting a certain equipment piece
        hit = True
        message = (self.m_name + " casts " + next_skill["Name"] + ", ")
        if "Target" in next_skill:
            # If target has equipment and the equipped item slot is not empty
            if target.has_equipment() and target.get_equipment(next_skill["Target"]) != -1:
                hit = False
                message += (ItemInfo.eq_loc_names[next_skill["Target"]] + " blocks the attack!")
            else:
                message += ("You do not have " + ItemInfo.eq_loc_names[next_skill["Target"]] + " equipped!\n")
        if hit:
            hitmsg = next_skill["MessageIfHit"]
            hitmsg = hitmsg.replace("%c", self.get_name(), 1)
            hitmsg = hitmsg.replace("%t", target.get_name(), 1)
            message += hitmsg
            # deal appropriate damage
            if next_skill["Damage"] == "Fatal":
                target.kill()
            elif next_skill["Damage"] == "Strength":
                target.take_damage(self.m_strength)
            elif next_skill["Damage"].isnumeric():
                target.take_damage(int(next_skill["Damage"]))
            else:
                print("Unhandled Damage Type:", next_skill["Damage"])
        return message

    # void - update character stats with equipment bonuses
    def update_stats(self):
        self.m_strength = self.m_base_str
        self.m_defense = self.m_base_def
        if self.m_hasEquipment:
            for i in range(len(self.m_equipment)):
                if "Strength" in ItemInfo.List[self.m_equipment[i]].m_stats.keys():
                    if ItemInfo.List[self.m_equipment[i]].m_stats["Strength"] >= 0:
                        self.m_strength += ItemInfo.List[self.m_equipment[i]].m_stats["Strength"]
                if "Defense" in ItemInfo.List[self.m_equipment[i]].m_stats.keys():
                    if ItemInfo.List[self.m_equipment[i]].m_stats["Defense"] >= 0:
                        self.m_defense += ItemInfo.List[self.m_equipment[i]].m_stats["Defense"]

    # Bool - Item is carried by character, worn or held
    def has_item(self, p_id):
        if self.has_inventory():
            for i in range(len(self.m_inventory)):
                if self.m_inventory[i] == p_id:
                    return True, 0
        if self.has_equipment():
            for i in range(len(self.m_equipment)):
                if self.m_equipment[i] == p_id:
                    return True, 1
        return False, -1

    # int - Search INV/EQ for item of given name and return the item id if found
    def find_item_by_name(self, p_itemname):
        if self.has_inventory():
            for i in range(len(self.m_inventory)):
                if str.find(ItemInfo.List[self.m_inventory[i]].getname().lower(), p_itemname) != -1:
                    return self.m_inventory[i]
        if self.has_equipment():
            for i in range(len(self.m_equipment)):
                if self.m_equipment[i] != -1:
                    if str.find(ItemInfo.List[self.m_equipment[i]].getname().lower(), p_itemname) != -1:
                        return self.m_equipment[i]
        return -1

    # void - Wear owned equipment
    def equip(self, item_id):
        have, where = self.has_item(item_id)
        if not have:
            print("You do not have that item.")
            return
        elif where != 0:  # Not in inventory, thus already worn
            print("That is already equipped.")
            return
        item_slot = ItemInfo.List[item_id].m_eq_slot
        if item_slot != 6:  # Items do not get equipped
            # Remove new item from inventory
            self.m_inventory.remove(item_id)
            # Slot not empty, put equipped item into inventory
            if self.m_equipment[item_slot] != -1:
                self.m_inventory.append(self.m_equipment[item_slot])
            # Equip new item
            self.m_equipment[item_slot] = item_id
            print("You equip", ItemInfo.List[item_id].getname() + ".")
        self.update_stats()

    # void - Delete character spellbook
    def reset_spellbook(self):
        self.m_SpellBook = [0]

    # void - add spell to spellbook from spellObject
    def add_spell(self, spell):
        self.m_SpellBook.append(spell)

    # void - add spell to spellbook from spell parameters
    def add_new_spell(self, p_name, p_msg_if_hit="%c strikes at %t.", p_damage_type="Strength", p_target_eq=-1):
        spell = {"Name": p_name, "MessageIfHit": p_msg_if_hit, "Damage": p_damage_type}
        if p_target_eq >= 0:
            spell["Target"] = p_target_eq
        self.add_spell(spell)


###############################################################################################################
# Player
###############################################################################################################


class PlayerInfo(CharacterInfo):
    flag_autoequip = False

    # Initialisation
    def __init__(self, p_name="Player", p_location="Secret Passage", p_description=""):
        CharacterInfo.__init__(self, p_name, 0, p_location, p_description)
        self.flag_autoequip = main.debug
        self.set_stats(60, 5, 5)
        self.reset_spellbook()
        self.add_new_spell("Attack", "%c strikes at %t.", "Strength")

    # void - pick up item. if Autoequip active, equip it.
    def get(self, item_id, p_from_object=None):
        if p_from_object is not None:
            p_from_object.m_Contents.remove(item_id)
        self.add_item(item_id)
        # Auto-Equip - if auto-equip is active and item can be equipped
        if self.flag_autoequip and (0 <= ItemInfo.List[item_id].m_eq_slot <= 5):
            auto_eq = "n"
            if self.get_equipment(ItemInfo.List[item_id].m_eq_slot) < item_id:  # If a weaker item is equipped
                auto_eq = "y"
            else:
                # If new item is weaker, confirm it to be equipped
                auto_eq = input("Equip " + ItemInfo.List[item_id].getname() + "?")
            auto_eq.lower()
            if auto_eq == "y" or auto_eq == "yes":
                self.equip(item_id)

    # void - toggle Autoequip flag
    def toggle_autoeq(self):
        self.flag_autoequip = not self.flag_autoequip
        print("Auto-Equip set to " + str(self.flag_autoequip) + ".")

###############################################################################################################
# Villain
###############################################################################################################


class VillainInfo(CharacterInfo):

    # Initialisation
    def __init__(self, p_name, p_location="Throne Room", p_description=""):
        CharacterInfo.__init__(self, p_name, 0, p_location, p_description)
        self.set_stats(50, 15, 3)
        # Construct the villain's Spellbook
        self.reset_spellbook()
        self.add_new_spell("Fireball",
                           "Fireball toasts you inside your armor, and you are slain.",
                           "Fatal", 1)
        self.add_new_spell("Ice Spike",
                           "An ice spike pierces your lung, and you are slain.",
                           "Fatal", 2)
        self.add_new_spell("Caustic Spray",
                           "A caustic spray blinds you, and you are slain.",
                           "Fatal", 3)
        self.add_new_spell("Foot Arrow",
                           "You take an arrow to the foot and are incapacitated. You are slain.",
                           "Fatal", 4)
        self.add_new_spell("Dark Aura",
                           "Dark aura saps away your life energy. You are slain.",
                           "Fatal", 5)
        self.add_new_spell("Fatigue",
                           "You slap the villain. Repeatedly. You grow tired and cannot continue. You are slain.",
                           "Fatal", 0)
        self.add_new_spell("Attack",
                           "A magic missile is cast at you.",
                           "Strength")
