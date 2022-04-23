from Room import *

class Dungeon:
    def __init__(self):
        self.players = []
        self.rooms = [Room("Entrance", None, "06", None, "01", [], []), \
                      Room("01", "02", "Entrance", "08", None, [], []), \
                      Room("02", None, "03", "01", None, [], []), \
                      Room("03", "11", "04", None, "02", [], []), \
                      Room("04", None, "05", "06", "03", [], []), \
                      Room("05", None, None, None, "04", [], []), \
                      Room("06", "04", None, "07", "Entrance", [], []), \
                      Room("07", "06", None, None, None, [], []), \
                      Room("08", "01", "09", "10", None, [], []), \
                      Room("09", None, None, None, "08", [], []), \
                      Room("10", "08", None, None, None, [], []), \
                      Room("11", "13", None, "03", "12", [], []), \
                      Room("12", None, "11", None, None, [], []), 
                      Room("13", None, None, "03", None, [], [])]

    def addPlayer(self, username):
        self.players.append(username)

    def removePlayer(self, username):
        self.players.remove(username)

    def listPlayers(self):
        print(self.players)

    def handleMessage(self, message):
        message = message.split(",")
        if message[0] == "attack":
            pass

        elif message[0] == "look":
            # This would be a string sent back to the player
            print("===== " + "roomname" + " =====")

        elif message[0] == "move":
            adjacent = self.rooms[0].adjacentRooms()
            if message[1] == "north":
                if adjacent[0] == None:
                    # This would be a string sent back to the player
                    print("There's no room over there")
                else:
                    # Move player to room
                    [ass]

            elif message[1] == "east":
                pass

            elif message[1] == "south":
                pass

            elif message[1] == "west":
                pass

            else:
                # This would be a string sent back to the player
                print("Could not interpret that command, type help to show \
                       list of possible commands.")

        elif message[0] == "get":
            pass

        elif message[0] == "info":
            # This would be a string sent back to the player
            print("item name" + ": ")

        elif message[0] == "drink":
            pass
            
        else:
            # This would be a string sent back to the player
            print("Could not interpret that command, type help to show \
                    list of possible commands.")

## Testing
if __name__ == "__main__":
    dungeon = Dungeon()
    dungeon.addPlayer("one")
    dungeon.addPlayer("two")
    dungeon.removePlayer("two")
    dungeon.listPlayers()