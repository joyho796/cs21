from Room import *
from Enemy import *

class Dungeon:

    ITEMDICT = {
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
            "isWeapon" : False
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
        }
    }

    def __init__(self):
        self.players = {}
        self.rooms = [Room("Entrance", None, "06", None, "01", [], []), \
                      Room("01", "02", "Entrance", "08", None, [], []), \
                      Room("02", None, "03", "01", None, ["Dagger", "Dagger", "Potion"], [Enemy("Grunt", self.ENEMYDICT["Grunt"], [])]), \
                      Room("03", "11", "04", None, "02", ["Dagger"], [Enemy("Grunt", self.ENEMYDICT["Grunt"], ["Potion"])]), \
                      Room("04", None, "05", "06", "03", ["Potion"], [Enemy("Grunt", self.ENEMYDICT["Grunt"], ["Sword"])]), \
                      Room("05", None, None, None, "04", ["Potion", "Sword"], [Enemy("Ooze", self.ENEMYDICT["Ooze"], ["Sword"])]), \
                      Room("06", "04", None, "07", "Entrance", [], [Enemy("Grunt", self.ENEMYDICT["Grunt"], ["Potion"])]), \
                      Room("07", "06", None, None, None, [], [Enemy("Grunt", self.ENEMYDICT["Grunt"], ["Sword"])]), \
                      Room("08", "01", "09", "10", None, ["Dagger"], []), \
                      Room("09", None, None, None, "08", [], [Enemy("Ooze", self.ENEMYDICT["Ooze"], ["Potion"])]), \
                      Room("10", "08", None, None, None, [], [Enemy("Ooze", self.ENEMYDICT["Ooze"], ["Potion"])]), \
                      Room("11", "13", None, "03", "12", ["Potion", "Sword"], []), \
                      Room("12", None, "11", None, None, [], [Enemy("Ooze", self.ENEMYDICT["Ooze"], ["Potion"])]),
                      Room("13", None, None, "03", None, [], [Enemy("Ooze", self.ENEMYDICT["Ooze"], ["Potion"])])]

    ##########################################################################
    # Given the name of a room, returns its index in the room array
    ##########################################################################
    def getRoomIndex(self, room):
        if (room == "Entrance"):
            return 0
        elif (room[0] == "0"):
            return int(room)

    ##########################################################################
    # Adds a player to the dungeon. By default, players start in the Entrance
    # (room 0)
    ##########################################################################
    def addPlayer(self, username):
        self.players[username] = 0

    def removePlayer(self, username):
        self.players.remove(username)

    def getPlayers(self):
        output = "Players in dungeon are: "
        for player in self.players:
            output += player + ", "

        output = output[:len(output) - 2]

        return output

    def handleMessage(self, player, message):
        room = self.rooms[self.players[player]]

        message = message.split(",")

        if message[0] == "attack":
            if len(message) > 2:
                attackDmg = Item.getDamage(message[2])
            else:
                attackDmg = Item.getDamage(message[1])
            attackDmg = random.randint(1, attackDmg)

            if len(room.enemies) > 0:
                room.enemies[0].takeDamage(attackDmg)
                return attackDmg
            else:
                return "There's no enemies here, you can relax"

        elif message[0] == "look":
            desc = []
            desc.append("========== Room [" + room.roomName + "] ==========")
            desc.append("| Enemies present: " + str(len(room.enemies)))
            desc.append("| Items present: " + str(len(room.items)))
            desc.append("| Rooms adjacent: " + str(room.countAdjacent()))
            desc.append("=========================")
            # This would be a list of strings sent back to the player
            return(desc)

        elif message[0] == "move":
            adjacent = room.getAdjacent()
            if message[1] == "north":
                if adjacent[0] == None:
                    return ("There's no room over there")
                else:
                    self.players[player] = self.getRoomIndex(adjacent[0])
                    return adjacent[0]
            elif message[1] == "east":
                if adjacent[1] == None:
                    return ("There's no room over there")
                else:
                    self.players[player] = self.getRoomIndex(adjacent[1])
                    return adjacent[1]
            elif message[1] == "south":
                if adjacent[2] == None:
                    return ("There's no room over there")
                else:
                    self.players[player] = self.getRoomIndex(adjacent[2])
                    return adjacent[2]
            elif message[1] == "west":
                if adjacent[3] == None:
                    return ("There's no room over there")
                else:
                    self.players[player] = self.getRoomIndex(adjacent[3])
                    return adjacent[3]
            else:
                # for debugging
                return("Could not interpret that command.")

        elif message[0] == "get":
            if message[1] in self.ITEMDICT:
                if room.hasItem(message[1]):
                    room.removeItem(message[1])
                    return message[1]
                else:
                    return "Item not in room. "
            else:
                return "Item not recognized. "

        elif message[0] == "info":
            if (message[1] in self.ITEMDICT):
                return self.ITEMDICT[message[1]]["description"]
            else:
                return "Given item not recognized."

        elif message[0] == "drink":
            minRoll = self.ITEMDICT[message[1]]["minRoll"]
            maxRoll = self.ITEMDICT[message[1]]["maxRoll"]
            return random.randint(minRoll, maxRoll)
