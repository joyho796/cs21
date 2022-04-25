from Room import *
from Enemy import *

class Dungeon:
    def __init__(self):
        self.players = {}
        self.rooms = [Room("Entrance", None, "06", None, "01", [], []), \
                      Room("01", "02", "Entrance", "08", None, [], []), \
                      Room("02", None, "03", "01", None, [Item("Dagger"), Item("Dagger"), Item("Potion")], [Enemy("E1", 1, None)]), \
                      Room("03", "11", "04", None, "02", [Item("Dagger")], [Enemy("E1", 2, Item("Potion"))]), \
                      Room("04", None, "05", "06", "03", [Item("Potion")], [Enemy("E1", 4, Item("Sword"))]), \
                      Room("05", None, None, None, "04", [Item("Potion"), Item("Sword")], [Enemy("E2", 6, Item("Sword"))]), \
                      Room("06", "04", None, "07", "Entrance", [], [Enemy("E1", 1, Item("Potion"))]), \
                      Room("07", "06", None, None, None, [], [Enemy("E1", 3, Item("Sword"))]), \
                      Room("08", "01", "09", "10", None, [Item("Dagger")], []), \
                      Room("09", None, None, None, "08", [], [Enemy("E2", 7, Item("Potion"))]), \
                      Room("10", "08", None, None, None, [], [Enemy("E2", 10, Item("Potion"))]), \
                      Room("11", "13", None, "03", "12", [Item("Potion"), Item("Sword")], []), \
                      Room("12", None, "11", None, None, [], [Enemy("E2", 6, Item("Potion"))]),
                      Room("13", None, None, "03", None, [], [Enemy("E2", 16, Item("Potion"))])]

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
            desc.append("======== Room [" + room.roomName + "] ========")
            desc.append("| Enemies present: " + str(len(room.enemies)))
            desc.append("| Items present: " + str(len(room.items)))
            desc.append("| Rooms adjacent: " + str(room.countAdjacent()))
            desc.append("==========================")
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
                # This would be a string sent back to the player
                return("Could not interpret that command.")

        elif message[0] == "get":
            if message[1] == "Sword":
                print("Acquired Sword") if room.hasItem("Sword") \
                else print("There's no Sword here")
            elif message[1] == "Dagger":
                print("Acquired Dagger") if room.hasItem("Dagger") \
                else print("There's no Dagger here")
            elif message[1] == "Potion":
                print("Acquired Potion") if room.hasItem("Potion") \
                else print("There's no Potion here")
            else:
                print("Could not understand message")

        elif message[0] == "info":
            return(Item(message[1]).Description)

        elif message[0] == "drink":
            pass

## Testing
#if __name__ == "__main__":
    #dungeon = Dungeon()
    #dungeon.addPlayer("one")
    #dungeon.addPlayer("two")
    #dungeon.removePlayer("two")
    #dungeon.listPlayers()
    #dungeon.handleMessage("player", "attack", 2)
    #dungeon.handleMessage("player", "attack", 1)
    #dungeon.handleMessage("player", "look", 2)
    #dungeon.handleMessage("player", "look", 11)
    #dungeon.handleMessage("player", "move,north", 11)
    #dungeon.handleMessage("player", "move,east", 11)
    #dungeon.handleMessage("player", "move,south", 11)
    #dungeon.handleMessage("player", "help", 11)
    #dungeon.handleMessage("player", "get,Sword", 11)
    #dungeon.handleMessage("player", "get,Sword", 4)
    #dungeon.handleMessage("player", "get,Potion", 4)
    #dungeon.handleMessage("player", "info,Potion", 4)

    #def listPlayers(self):
    #    print("Players in dungeon: ", self.players)
