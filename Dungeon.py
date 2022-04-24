from Room import *
from Enemy import *

class Dungeon:
    def __init__(self):
        self.players = []
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

    def addPlayer(self, username):
        self.players.append(username)

    def removePlayer(self, username):
        self.players.remove(username)

    def listPlayers(self):
        print("Players in dungeon: ", self.players)

    def handleMessage(self, player, message, room):
        room = self.rooms[room]
        message = message.split(",")
        if message[0] == "attack":
            attackDmg = 3
            if len(room.enemies) > 0:
                room.enemies[0].takeDamage(attackDmg)
                print("Dealt", attackDmg, "damage on enemy")
            else:
                print("There's no enemies here, you can relax")

        elif message[0] == "look":
            desc = "\n"
            desc += "    ======== Room [" + room.roomName + "] ========\n"
            desc += "    |                         |\n"
            desc += "    |   Enemies present:  " + str(len(room.enemies)) + "   |\n"
            desc += "    |   Items present:    " + str(len(room.items)) + "   |\n"
            desc += "    |   Rooms adjacent:   " + str(room.countAdjacent()) + "   |\n"
            desc += "    |                         |\n"
            desc +="    ===========================\n\n"
            # This would be a string sent back to the player
            print(desc)

        elif message[0] == "move":
            adjacent = room.getAdjacent()
            if message[1] == "north":
                print("There's no room over there") \
                if adjacent[0] == None \
                else print("Moved", player, message[1].capitalize(), "to Room", adjacent[0])
            elif message[1] == "east":
                print("There's no room over there") \
                if adjacent[1] == None \
                else print("Moved", player, message[1].capitalize(), "to Room", adjacent[1])
            elif message[1] == "south":
                print("There's no room over there") \
                if adjacent[2] == None \
                else print("Moved", player, message[1].capitalize(), "to Room", adjacent[2])
            elif message[1] == "west":
                print("There's no room over there") \
                if adjacent[3] == None \
                else print("Moved", player, message[1].capitalize(), "to Room", adjacent[3])
            else:
                # This would be a string sent back to the player
                print("Could not interpret that command, type help to show list of possible commands.")

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
            print(Item(message[1]).Description)

        elif message[0] == "drink":
            pass

        elif message[0] == "help":
            desc = "\n"
            desc += "    ========= Commands =========\n"
            desc += "    |                          |\n"
            desc += "    |  attack, look, move, get |\n"
            desc += "    |  info, drink             |\n"
            desc += "    |                          |\n"
            desc += "    ============================\n\n"
            # This would be a string sent back to the player
            print(desc)           
            
        else:
            # This would be a string sent back to the player
            print("Could not interpret that command, type help to show list of possible commands.")

## Testing
if __name__ == "__main__":
    dungeon = Dungeon()
    dungeon.addPlayer("one")
    dungeon.addPlayer("two")
    dungeon.removePlayer("two")
    dungeon.listPlayers()
    dungeon.handleMessage("player", "attack", 2)
    dungeon.handleMessage("player", "attack", 1)
    dungeon.handleMessage("player", "look", 2)
    dungeon.handleMessage("player", "look", 11)
    dungeon.handleMessage("player", "move,north", 11)
    dungeon.handleMessage("player", "move,east", 11)
    dungeon.handleMessage("player", "move,south", 11)
    dungeon.handleMessage("player", "help", 11)
    dungeon.handleMessage("player", "get,Sword", 11)
    dungeon.handleMessage("player", "get,Sword", 4)
    dungeon.handleMessage("player", "get,Potion", 4)
    dungeon.handleMessage("player", "info,Potion", 4)