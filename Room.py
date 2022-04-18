class Room:
    def __init__(roomName):
        self.roomName = roomName
        self.items = []
        self.adjacentRooms = [None, None, None, None]
        self.enemies = []