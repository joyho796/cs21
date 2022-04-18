class Room:
    def __init__(self, roomName, north, east, south, west, items, enemies):
        self.roomName = roomName
        self.adjacentRooms = [north, east, south, west]
        self.items = []
        self.enemies = []

    def getAdjacent(self):
        return self.adjacentRooms