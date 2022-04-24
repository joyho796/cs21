from Item import *

class Enemy:
    Name = ""
    Description = ""
    DescriptionDict = {"E1": "Your basic grunt. Nothing to worry about",
                       "E2": "Having fed on the other creatures for years now, this one packs a punch."}
    MaxDamage = 0
    DroppedItem = None
    HP = 100

    def __init__(self, Name, MaxDamage, DroppedItem):
        self.Name = Name
        self.Description = self.DescriptionDict[Name]
        self.MaxDamage = MaxDamage
        self.DroppedItem = DroppedItem

    def takeDamage(self, attackVal):
        self.HP = self.HP - attackVal

    def getName(self):
        return self.Name

    def getDescription(self):
        return self.Description

    def getMaxDamage(self):
        return self.MaxDamage
    
    def getHP(self):
        return self.HP
        