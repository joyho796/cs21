class Room:
    def __init__(self, roomName, north, east, south, west, items, enemies):
        self.roomName = roomName
        self.adjacentRooms = [north, east, south, west]
        self.items = items
        self.enemies = enemies

    def getAdjacent(self):
        return self.adjacentRooms

    def countAdjacent(self):
        count = 0
        for direction in self.adjacentRooms:
            if direction != None:
                count = count + 1
        return count

    def hasItem(self, name):
        for item in self.items:
            if item.Name == name:
                return True
        return False