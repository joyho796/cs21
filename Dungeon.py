##########################################################################
# Class: Dungeon
# Used to manage the setup and current state of the dungeon.
##########################################################################

from Room import *
from Enemy import *
from Player import *
import random

class Dungeon:

    ITEMDICT = {
        "Fist" : {
            "description" : "It's your own fist. You should be familiar with it. ",
            "minRoll" : 1,
            "maxRoll" : 2,
            "isWeapon" : True
        },
        "Knife" : {
            "description" : "A small penknife. Honestly, it's better suited for whittling than combat. ",
            "minRoll" : 2,
            "maxRoll" : 8,
            "isWeapon" : True
        },
        "Sword" : {
            "description" : "An ordinary sword. Though it's been long since its glory days, the blade remains sharp.",
            "minRoll" : 5,
            "maxRoll" : 20,
            "isWeapon" : True
        },
        "Dagger" : {
            "description" : "An assassins dagger. Chips have begun to form along its edge, but it remains a trusty tool.",
            "minRoll" : 12,
            "maxRoll" : 15,
            "isWeapon" : True
        },
        "Glaive" : {
            "description" : "A polearm with an elegant blade affixed to the end. While beautiful, it looks deadly.",
            "minRoll" : 20,
            "maxRoll" : 30,
            "isWeapon" : True
        },
        "Potion" : {
            "description" : "A healing potion. It says healing on the red bottle, so it should be fine, right?",
            "minRoll" : 15,
            "maxRoll" : 20,
            "isWeapon" : False
        }
    }

    ENEMYDICT = {
        "Grunt" : {
            "description" : "Your basic grunt. Nothing to worry about",
            "maxDamage" : 10,
            "minDamage" : 5,
            "hp" : 20
        },
        "Ooze" : {
            "description" : "Having fed on the other creatures for years now, this one packs a punch.",
            "maxDamage" : 20,
            "minDamage" : 15,
            "hp" : 30
        },
        "Rat_swarm" : {
            "description" : "A seething mass of rats. Ew",
            "maxDamage" : 10,
            "minDamage" : 5,
            "hp" : 30
        },
        "Skeleton" : {
            "description" : "The shambling, yellowing remains of what might have once been another adventurer.",
            "maxDamage" : 25,
            "minDamage" : 10,
            "hp" : 45
        },
        "Dragon" : {
            "description" : "A colossal red beast snorting flames from its nostrils.",
            "maxDamage" : 50,
            "minDamage" : 10,
            "hp" : 60
        }
    }

    ROOMDESCRIPTIONSDICT = {
        "Entrance" : "This large room might once have been quite grand, with the fading murals on the walls and cracked pillars towering above you.",
        "01" : "The remains of a wooden chair lie crumpled in the corner. It might have been nice to have a seat, if it wasn't broken.",
        "02" : "A lovely moldering tapestry of a unicorn adorns the wall.",
        "03" : "A rat scampers across the floor.",
        "04" : "Something green drips down from the cieling.",
        "05" : "The edges of the door in this room boast beautiful carved trim of vines and flowers.",
        "06" : "Yellowing bones lie strewn across the floor, picked clean of flesh and skin.",
        "07" : "Relief sculptures of lions stand proud of the corners of the room.",
        "08" : "The walls appear blackened and scortched.",
        "09" : "Someone did a shoddy job of the masonry in this room.",
        "10" : "Broken glass covers the floor of this room. Tread carefully.",
        "11" : "Unlike most other rooms, which are carved from life stone, this room is almost cave-like.",
        "12" : "It smells weird in this room.",
        "13" : "This giant room is flooded with gold and jewels; you can't see any floor at all."
    }

    ##########################################################################
    # Constructor. Sets up the dungeon and its rooms.
    ##########################################################################
    def __init__(self):
        self.players = {}
        self.rooms = [Room("Entrance", None, "06", None, "01", [], []), \
                      Room("01", "02", "Entrance", "08", None, [], []), \
                      Room("02", None, "03", "01", None, ["Dagger", "Dagger", "Potion"], [Enemy("Grunt", self.ENEMYDICT["Grunt"], [])]), \
                      Room("03", "11", "04", None, "02", ["Dagger"], [Enemy("Grunt", self.ENEMYDICT["Grunt"], ["Potion"])]), \
                      Room("04", None, "05", "06", "03", ["Potion"], [Enemy("Grunt", self.ENEMYDICT["Grunt"], ["Sword"])]), \
                      Room("05", None, None, None, "04", ["Potion", "Sword"], [Enemy("Ooze", self.ENEMYDICT["Ooze"], ["Sword"])]), \
                      Room("06", "04", None, "07", "Entrance", [], [Enemy("Rat_swarm", self.ENEMYDICT["Rat_swarm"], ["Potion"])]), \
                      Room("07", "06", None, None, None, [], [Enemy("Grunt", self.ENEMYDICT["Grunt"], ["Glaive"])]), \
                      Room("08", "01", "09", "10", None, ["Dagger"], []), \
                      Room("09", None, None, None, "08", [], [Enemy("Skeleton", self.ENEMYDICT["Skeleton"], ["Potion"])]), \
                      Room("10", "08", None, None, None, [], [Enemy("Ooze", self.ENEMYDICT["Ooze"], ["Potion"])]), \
                      Room("11", "13", None, "03", "12", ["Potion", "Glaive"], []), \
                      Room("12", None, "11", None, None, [], [Enemy("Ooze", self.ENEMYDICT["Ooze"], ["Potion"])]),
                      Room("13", None, None, "03", None, [], [Enemy("Dragon", self.ENEMYDICT["Dragon"], ["Potion"])])]


    ##########################################################################
    # Takes: string (room name)
    # Returns: int (room index)
    # Does: Given the name of a room, returns its index in the room array
    ##########################################################################
    def getRoomIndex(self, room):
        if (room == "Entrance"):
            return 0
        else:
            return int(room)

    ##########################################################################
    # Takes: string (username)
    # Returns: None
    # Does: Adds a player to the dungeon. By default, players start in the
    # Entrance (room 0)
    ##########################################################################
    def addPlayer(self, username):
        self.players[username] = Player(username)
        self.rooms[0].addPlayer(username)

    ##########################################################################
    # Takes: string (username)
    # Returns: None
    # Does: Removes a player from the dungeon.
    ##########################################################################
    def removePlayer(self, username):
        if (username in self.players.keys()):
            roomIndex = self.players[username].getRoomNumber()
            self.rooms[roomIndex].removePlayer(username)
            del self.players[username]


    ##########################################################################
    # Takes: string (room name)
    # Returns: boolean
    # Does: Determines if there are players and enemies in the same room.
    ##########################################################################
    def playerAndEnemyInRoom(self, roomName):
        roomIndex = self.getRoomIndex(roomName)
        room = self.rooms[roomIndex]

        if (len(room.players) > 0) and (len(room.enemies) > 0):
            return True

        return False


    ##########################################################################
    # Takes: string (room name)
    # Returns: [string, string, int] (username, enemy name, damage amount)
    # Does:If there are players and enemies in the same room, selects a random
    # enemy to attack a random player.
    ##########################################################################
    def attackPlayerInRoom(self, roomName):
        roomIndex = self.getRoomIndex(roomName)
        room = self.rooms[roomIndex]

        player = random.choice(room.players)
        enemy = random.choice(room.enemies)

        maxDmg = self.ENEMYDICT[enemy.Name]["maxDamage"]
        minDmg = self.ENEMYDICT[enemy.Name]["minDamage"]
        attackDmg = random.randint(minDmg, maxDmg)

        state = self.players[player].takeDamage(attackDmg)

        return [player, enemy.Name, attackDmg, state]


    ##########################################################################
    # Takes: string (user name)
    # Returns: boolean
    # Does: Determines if a given player is in the dungeon
    ##########################################################################
    def isPlayerInDungeon(self, name):
        return name in self.players.keys()


    ##########################################################################
    ##########################################################################
    ## Start of section containing functions that respond to message prompts
    ## from the server
    ##########################################################################
    ##########################################################################


    ##########################################################################
    # Takes: string, string (username, username)
    # Returns: list
    # Does: Allows a player to attack an entity in a room, either an enemy or
    # another player.
    ##########################################################################
    def attack(self, player, target):
        room = self.rooms[self.players[player].room]

        weapon = self.players[player].currentWeapon
        maxDmg = self.ITEMDICT[weapon]["maxRoll"]
        minDmg = self.ITEMDICT[weapon]["minRoll"]
        attackDmg = random.randint(minDmg, maxDmg)

        # if no specific target given, attack enemy in the room, if any
        if target == None:
            if len(room.enemies) <= 0:
                return ["There's no enemies here, you can relax."]

            state = room.enemies[0].takeDamage(attackDmg)
            name = room.enemies[0].Name

            if state == "dead":
                droppedItems = room.enemies[0].DroppedItems
                room.items.extend(droppedItems)
                room.enemies.pop(0)

            return [room, attackDmg, name, state]

        # player wants to attack other player
        elif (target in self.players.keys()):
            state = self.players[target].takeDamage(attackDmg)
            return [room, attackDmg, target, state, "player"]

        return ["Target given not in room."]



    ##########################################################################
    # Takes: string (user name), string (item name)
    # Returns: string (result)
    # Does: Allows a user to drink a potion
    ##########################################################################
    def drink(self, player, item):
        item = item.capitalize()

        if len(self.players[player].potions) > 0:
            minRoll = self.ITEMDICT[item]["minRoll"]
            maxRoll = self.ITEMDICT[item]["maxRoll"]
            hp = random.randint(minRoll, maxRoll)
            self.players[player].heal(hp)
            self.players[player].potions.remove("Potion")
            return "You healed " + str(hp) + " HP!"
        else:
            return "You don't have any potions."


    ##########################################################################
    # Takes: string (user name), string (item name)
    # Returns: string (result)
    # Does: Allows a user to change their current weapon
    ##########################################################################
    def equip(self, player, item):
        item = item.capitalize()

        if (item in self.ITEMDICT and item != "Potion"):
            # makes sure they have the weapon they want to equip
            if item in self.players[player].weapons:
                self.players[player].currentWeapon = item
                return item + " equipped as weapon."
            else:
                return "You don't have a " + item + "."
        else:
            return "Weapon not recognized."


    ##########################################################################
    # Takes: string, string (username, item name)
    # Returns: string
    # Does: Adds a given item from the player's current room to their inventory,
    # if said item is in the room.
    ##########################################################################
    def get(self, player, item):
        item = item.capitalize()

        room = self.rooms[self.players[player].room]

        if item.capitalize() in self.ITEMDICT:
            if room.hasItem(item.capitalize()):
                room.removeItem(item.capitalize())
                if item.capitalize() == "Potion":
                    self.players[player].potions.append(item.capitalize())
                else:
                    self.players[player].weapons.append(item.capitalize())
                return "You picked up a " + item.capitalize() + "."
            else:
                return "Item not in room."
        else:
            return "Item not recognized."


    ##########################################################################
    # Takes: string (user name), string (user name), string (item name)
    # Returns: [string, boolean] (result, whether trade was successful)
    # Does: Allows a user to handoff one item to another user
    ##########################################################################
    def give(self, player, target, item):
        item = item.capitalize()

        # if player cannot give item
        if not(item in self.ITEMDICT):
            return ["Item not recognized.", False]
        elif not((item in self.players[player].weapons) or (item in self.players[player].potions)):
            return ["Item not in your inventory. ", False]

        room = self.rooms[self.players[player].room]

        # if indended recipient is not in room
        if (target in self.players.keys()):
            if target in room.players:
                self.players[player].removeItem(item)
                if (self.ITEMDICT[item]["isWeapon"]):
                    self.players[target].addWeapon(item)
                else: self.players[target].addPotion(item)
                return ["Item given."]
            return ["Player must be in your room to give items. ", False]

        return ["Player not in dungeon. ", False]


    ##########################################################################
    # Takes: string (item name)
    # Returns: string (item/enemy description)
    # Does: Returns information about a given item or enemy.
    ##########################################################################
    def info(self, item):
        item = item.capitalize()

        if (item in self.ITEMDICT.keys()):
            return self.ITEMDICT[item]["description"]
        elif (item in self.ENEMYDICT.keys()):
            return self.ENEMYDICT[item]["description"]
        else:
            return "Given item/enemy not recognized."


    ##########################################################################
    # Takes: string (username)
    # Returns: list strings (room description)
    # Does: Returns information about a given room.
    ##########################################################################
    def look(self, player):
        room = self.rooms[self.players[player].room]

        desc = ["==="]
        desc.append("Players present: " + str(len(room.players)))
        desc.append("Enemies present: " + room.getEnemies())
        desc.append("Items present: " + room.getItems())
        desc.append("Rooms adjacent: " + str(room.countAdjacent()))
        desc.append("Description: " + self.ROOMDESCRIPTIONSDICT[room.roomName])
        desc.append("=== Room " + room.roomName + " ===")
        # This would be a list of strings sent back to the player
        return(desc)


    ##########################################################################
    # Moves a player from one room to another
    ##########################################################################
    def move(self, player, direction):
        room = self.rooms[self.players[player].room]
        roomName = room.roomName

        adjacent = room.getAdjacent()

        if direction == "north":
            if adjacent[0] == None:
                return ["There's no room over there"]
            else:
                self.players[player].room = self.getRoomIndex(adjacent[0])
                room.removePlayer(player)
                self.rooms[self.getRoomIndex(adjacent[0])].addPlayer(player)
                return [roomName, adjacent[0]]
        elif direction == "east":
            if adjacent[1] == None:
                return ["There's no room over there"]
            else:
                self.players[player].room = self.getRoomIndex(adjacent[1])
                room.removePlayer(player)
                self.rooms[self.getRoomIndex(adjacent[1])].addPlayer(player)
                return [roomName, adjacent[1]]
        elif direction == "south":
            if adjacent[2] == None:
                return ["There's no room over there"]
            else:
                self.players[player].room = self.getRoomIndex(adjacent[2])
                room.removePlayer(player)
                self.rooms[self.getRoomIndex(adjacent[2])].addPlayer(player)
                return [roomName, adjacent[2]]
        elif direction == "west":
            if adjacent[3] == None:
                return ["There's no room over there"]
            else:
                self.players[player].room = self.getRoomIndex(adjacent[3])
                room.removePlayer(player)
                self.rooms[self.getRoomIndex(adjacent[3])].addPlayer(player)
                return [roomName, adjacent[3]]
        else:
            return ["Cannot move in that direction."]

    ##########################################################################
    # Returns a list of all players in the dungeon
    ##########################################################################
    def players(self):
        output = "Players in dungeon are: "
        for player in self.players:
            output += player + ", "

        output = output[:len(output) - 2]

        return output

    ##########################################################################
    # Returns a list of all players in the dungeon
    ##########################################################################
    def self(self, player):
        player = self.players[player]
        return str(player.hp) + ". " + player.currentWeapon + ". " + player.getInventory()
