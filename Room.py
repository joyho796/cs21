import time
class Room:
    def __init__(self, roomName, north, east, south, west, items, enemies):
        self.roomName = roomName
        self.adjacentRooms = [north, east, south, west]
        self.items = items
        self.enemies = enemies
        self.players = []

    def getAdjacent(self):
        return self.adjacentRooms

    def countAdjacent(self):
        count = 0
        for direction in self.adjacentRooms:
            if direction != None:
                count = count + 1
        return count

    def hasItem(self, name):
        if name in self.items:
                return True
        return False

    def removeItem(self, name):
        self.items.remove(name)

    def addPlayer(self, name):
        self.players.append(name)

    def removePlayer(self, name):
        self.players.remove(name)

    def getItems(self):
        output = ""
        for item in self.items:
            output += item + ", "

        output = output[:len(output) - 2]

        return output

    def getEnemies(self):
        output = ""
        for enemy in self.enemies:
            output += enemy.getName() + ", "

        output = output[:len(output) - 2]

        return output
