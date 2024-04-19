
exit_format = "NEWS"
exit_words = ["North", "East", "West", "South"]
exit_words_d = {
    "n": "North",
    "e": "East",
    "w": "West",
    "s": "South",
    "u": "Up",
    "d": "Down"
}

'''
class Room:
    m_ID = 0
    m_Name = "PLACEHOLDER_NAME"
    m_Desc = "PLACEHOLDER_DESCRIPTION"
    m_Contents = []
    m_Exits = []

    # initialisation
    def __init__(self, p_id, p_name, p_exits=None, p_desc="", p_contents=None):
        self.m_ID = p_id
        self.m_Name = p_name
        self.m_Desc = p_desc
        self.m_Contents = p_contents if p_contents is not None else []
        self.m_Exits = p_exits if p_exits is not None else [-1, -1, -1, -1]

    # Str - Returns the exit String for a room, ie: "NE S", " EW ", "NEWS"
    def print_exits(self):
        exits = ""
        for x in range(4):
            if self.m_Exits[x] != -1:
                exits += exit_format[x]
            else:
                exits += " "
        if exits == "    ":
            exits = "None."
        return exits

    # Void - Prints Room Info for describing a room upon entry
    def print_room(self):
        # print("Room", self.m_ID)
        print(("[" + str(self.m_ID) + "] " if main.debug else "") + self.m_Name)
        if self.m_Desc != "":
            print(self.m_Desc)
            print()
        print("Exits:", self.print_exits())
        # print contents
        if len(self.m_Contents) != 0:
            print("Room Contents:")
        for i in range(len(self.m_Contents)):
            print(" ", ItemInfo.List[self.m_Contents[i]].getname())
        print()

    # Int - Returns the roomID beyond a given exit, if exists
    def get_exit(self, exit_string):
        # cannot pass in anything besides n, e, w, s due to command parsing
        return self.m_Exits[str.find(exit_format.lower(), exit_string)]

    # Bool - Returns if room contains target item
    def contains_item(self, p_id):
        for i in range(len(self.m_Contents)):
            if self.m_Contents[i] == p_id:
                return True
        return False

    # void - add item to the room
    def drop(self, item_id):
        self.m_Contents.append(item_id)

    # void add a list of items to the room
    def drop_all(self, item_cache):
        for i in range(len(item_cache)):
            self.m_Contents.append(item_cache.pop())

'''
# Room Initialization


List = {
    "Secret Passage": {
        "id": 0,
        "s": "Bedroom",
        "view": "This is a hidden passageway into the castle. Dark and dreary, a dank, \n" +
                "musty smell permeates the air of the corridor. To the north, a slick \n" +
                "slope collapsed with rubble is responsible for the knock on your head. \n" +
                "You won't be going back that way. The only exit now is to continue on \n" +
                "south into the castle."
    },
    "Bedroom": {
        "id": 1,
        "n": "Secret Passage",
        "e": "Kitchen",
        "items": [4],
        "view": "This room belonged to a loyal servant, but you can't remember whom... \n" +
                "The meager furnishings belie the simple lifestyle of the former occupant. \n" +
                "Outside the door is a short hall leading east toward the kitchen. There \n" +
                "is another exit here that not many know of and hidden inside what looks \n" +
                "to be a wardrobe, leading north through a secret underground passage."
    },
    "Salon": {
        "id": 2,
        "e": "Main Foyer",
        "s": "Kitchen",
        "items": [5],
        "view": "The King's sitting room. Here he would entertain guests or sit and read \n" +
                "from the myriad of books lining the walls. A long sofa, chaise lounge \n" +
                "and sitting chair formed a half circle about the heart set into the \n" +
                "stone wall to the north. Amid the bookshelves, several curios sat on \n" +
                "display, now only collecting dust. A doorway to the south served for \n" +
                "quick delivery of food and drink from the kitchen, while to the east \n" +
                "lay the main foyer of the castle.",
    },
    "Kitchen": {
        "id": 3,
        "n": "Salon",
        "e": "Grand Hall",
        "w": "Bedroom",
        "items": [1, 13],
        "view": "This was a lively place. There were always cooks and staff bustling \n" +
                "about. Now it is cold and empty. The fires no longer burn in the potbelly \n" +
                "stoves. The washing basins are empty. Some food that was left has well \n" +
                "past rotted, what wasn't stripped clean by pests. Ingredient barrels line \n" +
                "one wall, once holding the suppers and breakfasts of the nobility and \n" +
                "staff that called this castle home. Through a doorway to the west can \n" +
                "be seen a hall leading to the servants rooms. Along the north wall, a \n" +
                "door leads to the King's salon. To the east, a door hangs precariously \n" +
                "from one hinge, beyond which you can see the grand hall.",
    },
    "Main Foyer": {
        "id": 4,
        "e": "Guard Room",
        "w": "Salon",
        "s": "Grand Hall",
        "items": [2, 17],
        "view": "This is the main entrance to the castle. The extravagant, imposing \n" +
                "doors lay to the north, completely destroyed and buried in fragments \n" +
                "of the wall that once stood over and around the heavy oaken slabs. \n" +
                "The prince's favorite suits of armor once lined the walls of this \n" +
                "room, however, only one remains, having been pilfered by militia \n" +
                "during the ill-fated defense of the castle. Along the east wall \n" +
                "stood a guard post, behind which is the door that leads to the guard \n" +
                "room. To the west, a door once bordered by fancy art leads to the \n" +
                "salon. Further south, a massive archway opens up to the even larger \n" +
                "grand hall."
    },
    "Grand Hall": {
        "id": 5,
        "n": "Main Foyer",
        "w": "Kitchen",
        "s": "Throne Room Approach",
        "items": [16, 15],
        "view": "THE Grand Hall. This is the biggest room in all the kingdom. Wider \n" +
                "than most homes and nearly as long as a city block. The ceiling gave \n" +
                "way to stained glass that depicted the great history of the country. \n" +
                "That is, before the invasion destroyed them all, shattering the past \n" +
                "literally as well as symbolically. Down the middle of the room runs \n" +
                "a beautiful rug, a delicate balance of color and imagery, though \n" +
                "covered in dust, still awe inspiring in its make. A door to the west \n" +
                "leads to the kitchen for direct access for when this room was used as \n" +
                "a dining hall for great events. Another door can barely made out along \n" +
                "the eastern wall, though it is subdued as if it is meant to not be \n" +
                "seen. To the north, a large archway funnels into the main foyer \n" +
                "leading to the castle's front entrance. Continuing south, you can see \n" +
                "the hallway leading to the throne room."
    },
    "Guard Room": {
        "id": 6,
        "w": "Main Foyer",
        "s": "Armory",
        "items": [3, 14],
        "view": "Dust hangs heavy in the air here, one of the first places to fall in \n" +
                "the invasion. Austere bunks line the walls of the guard room, providing \n" +
                "place for the soldiers defending the castle to rest and recuperate. \n" +
                "The door to the west leads to the gard post in the main foyer, while \n" +
                "the door at the back of the room to the south grants access to what used \n" +
                "to be the armory. During the invasion, everything that was in this room \n" +
                "was put to use defending against the siege. Nothing remains but a \n" +
                "storage crate and an old helmet."
    },
    "Armory": {
        "id": 7,
        "n": "Guard Room",
        "items": [0],
        "view": "The armory is a small room lined with rows upon rows of weapon racks \n" +
                "and armor stands. Many of these racks and stands are now toppled, \n" +
                "tossed and destroyed by the invaders claiming everything they could. \n" +
                "At the base of a fallen rack can be seen the glint of forgotten steel."
    },
    "Throne Room Approach": {
        "id": 8,
        "n": "Grand Hall",
        "s": "Throne Room",
        "items": [18],
        "view": "The hallway leading to the throne room was lined with many of the \n" +
                "great works of art and rare relics that the country had produced. \n" +
                "All of which were not gone or destroyed. Even the tables that held \n" +
                "them have been upturned and shattered. Among the rubble and debris, \n" +
                "the withering bodies of defending guards and adventurers like you lay \n" +
                "lifeless. To the north, the great hall lies, the light shining through \n" +
                "the open ceiling still covering the room in a gray pallor. To the \n" +
                "south is the Throne Room. And your very fate itself. \n" +
                "This is where it gets real."
    },
    "Throne Room": {
        "id": 9,
        "n": "Throne Room Approach",
        "chars": "Villain",
        "view": "The Throne room. The seat of power. This room was unrivalled in its \n" +
                "opulence, the very walls being adorned with rare gems and lined with \n" +
                "gold. All of which have since been stripped or tarnished. Now the \n" +
                "glorious seat of the king sits atop the platform surrounded by dismay \n" +
                "and death. This room once held the hope of the kingdom.\n" +
                "\n" +
                "Now it only smells strongly of unwashed feet and broken dreams."
    }
}
