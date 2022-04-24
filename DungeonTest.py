class Dungeon:
    def __init__(self):
        self.players = []
        self.introMessage = "You enter the dungeon in room1."

    def addPlayer(self, userName):
        self.players.append(userName)


    def getPlayers(self):
        output = "Players in dungeon are: "
        for player in self.players:
            output += player + ", "

        output = output[:len(output) - 2]

        return output

    def getIntro(self):
        return self.introMessage
