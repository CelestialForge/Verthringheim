import RoomInfo
import main

eq_loc_names = ["Weapon", "Shield", "Armor", "Helm", "Boots", "Amulet", "Book", "Scroll"]
WEAPON = 0
SHIELD = 1
ARMOR = 2
HELM = 3
BOOTS = 4
AMULET = 5
BOOK = 6  # Read lore
SCROLL = 7  # Learn Spells
CONTAINER = -1


def get_item(item_id):
    return List[item_id]


class ItemInfo:
    m_id = 0
    m_name = ""
    m_desc = ""
    m_eq_slot = -1
    m_contains = []
    m_Contents = []
    m_hides = []
    m_stats = {}

    # initialization
    def __init__(self,
                 p_id,
                 p_name,
                 p_slot=-1,
                 p_desc="",
                 p_stats=None,
                 p_in=None,
                 p_under=None):
        self.m_id = p_id
        self.m_name = p_name
        self.m_desc = p_desc
        if self.m_desc == "":
            self.m_desc = self.m_name
        self.m_eq_slot = p_slot
        self.m_stats = p_stats if p_stats is not None else {}
        self.m_Contents = p_in if p_in is not None else []
        self.m_hides = p_under if p_under is not None else []

    # debug printing of all object data
    def print_item(self):
        print("ID:", self.m_id)
        print("Name:", self.m_name)
        if self.m_eq_slot != -1:
            print("Equip Slot:", eq_loc_names[self.m_eq_slot])
        else:
            print("Container")
        print(self.m_desc)
        print(self.m_stats)
        self.look_in()
        self.look_under()

    # print visual inspection
    def look_at(self):
        print(self.m_desc)
        if self.has_contents():
            print("Seems like there is something inside...")
        if self.has_hidden():
            print("Something appears hidden underneath...")

    # print what, if anything, is inside
    def look_in(self):
        if self.has_contents():
            print("Contained inside", self.m_name + ", you find:")
            for i in range(len(self.m_Contents)):
                print("  " + List[self.m_Contents[i]].getname())
        else:
            print("There is nothing inside.")

    # print what, if anything, is underneath
    def look_under(self):
        if self.has_hidden():
            print("Hidden underneath", self.m_name + ", you find:")
            for i in range(len(self.m_hides)):
                print("  " + List[self.m_hides[i]].getname())
            print("Use [MOVE] + item name or ID to reveal these items!")
        else:
            print("There is nothing underneath.")

    # Return the object's name
    def getname(self):
        return ("[" + str(self.m_id) + "] " if main.debug else "") + self.m_name

    # Container has contents inside
    def has_contents(self):
        return len(self.m_Contents) > 0

    # Container has hidden contents
    def has_hidden(self):
        return len(self.m_hides) > 0

    # determine if an item can be worn
    def can_equip(self):
        return 0 <= self.m_eq_slot <= 5

    # Use Item
    def use(self):
        if self.m_eq_slot == BOOK:  # Use == Read
            self.look_at()
        else:
            # do action
            pass

    # Remove and return all items contained inside
    def dump_all(self):
        r_contents = self.m_Contents
        self.m_contains = []
        return r_contents

    # Remove and return all items hidden underneath
    def find_all(self):
        r_contents = self.m_hides
        self.m_hides = []
        return r_contents

    # Determine if the target item is inside this item
    def has_item(self, item_id):
        if self.has_contents():
            for i in range(len(self.m_Contents)):
                if self.m_Contents[i] == item_id:
                    return True
            return False

    # Update Map Item's description to show player location
    def update_map(self, p_player_loc):
        loc_id = RoomInfo.List[p_player_loc]['id']
        layout = [  # Room IDs
            [0, 2, 4, 6],
            [1, 3, 5, 7],
            [-1, -1, 8, -1],
            [-1, -1, 9, -1]
        ]
        map_loc = [-1, -1]
        map_result = ""
        base_map = [  # blank map
            "[ ] [ ]-[ ]-[ ]\n",
            " |   |   |   | \n",
            "[ ]-[ ]-[ ] [ ]\n",
            "         |     \n",
            "        [ ]    \n",
            "         |     \n",
            "        [ ]    \n"
        ]
        # Find Player's "world coordinates"
        for y in range(len(layout)):
            for x in range(len(layout[y])):
                if loc_id == layout[y][x]:
                    map_loc = [x, y]
                    break
            if map_loc[1] != -1:
                break
        # convert "world coordinates" to map coordinates
        map_loc = [(map_loc[0] * 4) + 1, map_loc[1] * 2]
        # copy base map to map, except where player is
        for i in range(len(base_map)):  # row/y
            for j in range(len(base_map[i])):  # col/x
                if i == map_loc[1] and j == map_loc[0]:
                    map_result += "X"
                else:
                    map_result += base_map[i][j]

        # save the new map
        self.m_desc = p_player_loc + \
            "\n" + \
            map_result + \
            "\nX: You are here"


"""
    ItemInfo:
            p_id,
            p_name,
            p_slot=-1,
            p_desc="",
            p_stats=None,
            p_in=None,
            p_under=None):
"""
# Item List Initialization
List = [
    # Equipment
    ItemInfo(0, "Basic Sword",
             WEAPON,
             "", {"Strength": 1}),
    ItemInfo(1, "Basic Shield",
             SHIELD,
             "", {"Defense": 1}),
    ItemInfo(2, "Basic Armor",
             ARMOR,
             "", {"Defense": 1}),
    ItemInfo(3, "Basic Helm",
             HELM,
             "", {"Defense": 1}),
    ItemInfo(4, "Basic Boots",
             BOOTS,
             "", {"Defense": 1}),
    ItemInfo(5, "Basic Amulet",
             AMULET,
             "", {"Defense": 1}),
    ItemInfo(6, "Epic Longsword Of Doom",
             WEAPON,
             "", {"Strength": 2}),
    ItemInfo(7, "Impenetrable Mirror Shield of the Bulwark",
             SHIELD,
             "", {"Defense": 2}),
    ItemInfo(8, "Valiant Mythril Armor of Radiance",
             ARMOR,
             "", {"Defense": 2}),
    ItemInfo(9, "Enlightened Helmet of Inspiration",
             HELM,
             "", {"Defense": 2}),
    ItemInfo(10, "Unstoppable Light Boots of the Wind",
             BOOTS,
             "", {"Defense": 2}),
    ItemInfo(11, "Divine Amulet of Protective Grace",
             AMULET,
             "", {"Defense": 2}),
    ItemInfo(12, "Invincible",
             WEAPON,
             "This sword shines with a holy light.", {"Strength": 5}),
    # Containers
    ItemInfo(13, "Barrel",
             CONTAINER,
             "A weathered, waterlogged barrel. Mayhaps something is still inside?",
             p_in=[10],
             p_under=[19]),
    ItemInfo(14, "Crate",
             CONTAINER,
             "An old, tattered crate. The top is missing, revealing its contents.",
             p_in=[7],
             p_under=[6]),
    ItemInfo(15, "An Ornate Rug",
             CONTAINER,
             "A beautifully woven rug with a myriad of colors and intricate designs.",
             p_under=[11]),
    ItemInfo(16, "Closet Door",
             CONTAINER,
             "There is a door here that is subdued. Almost as if it were only a cleaning closet.",
             p_in=[8]),
    ItemInfo(17, "Armor Stand",
             CONTAINER,
             "This stand holds up a suit of armor.",
             p_under=[9]),
    ItemInfo(18, "A Heap of Fallen Adventurers",
             CONTAINER,
             "You aren't the first person to attempt this quest. Something tells you that you should be\n" +
             "fully prepared before proceeding further...",
             p_under=[12]),
    # Items
    ItemInfo(19, "Map",
             BOOK,
             ""),
]
