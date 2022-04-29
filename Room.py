import time
class Room:
    def __init__(self, roomName, north, east, south, west, items, enemies):
        self.roomName = roomName
        self.adjacentRooms = [north, east, south, west]
        self.items = items
        self.enemies = enemies
        self.players = []

    # Returns the list of adjacent rooms
    def getAdjacent(self):
        return self.adjacentRooms

    # Counts the number of adjacent rooms
    def countAdjacent(self):
        count = 0
        for direction in self.adjacentRooms:
            if direction != None:
                count = count + 1
        return count

    # Determines if a room has an item
    def hasItem(self, name):
        if name in self.items:
                return True
        return False

    # removes an item from a room
    def removeItem(self, name):
        self.items.remove(name)

    # adds a player to a room
    def addPlayer(self, name):
        self.players.append(name)

    # removes a player from the room
    def removePlayer(self, name):
        self.players.remove(name)

    # returns a list of the items in the room as a string
    def getItems(self):
        output = ""
        for item in self.items:
            output += item + ", "

        output = output[:len(output) - 2]

        return output

    # returns a list of items in the room as a string
    def getEnemies(self):
        output = ""
        for enemy in self.enemies:
            output += enemy.getName() + ", "

        output = output[:len(output) - 2]

        return output

    # determines if there are any enemies present in the room.
    def hasEnemy(self):
        if (len(self.enemies) > 0):
            return True

        return False
