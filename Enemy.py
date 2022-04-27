from Item import *

class Enemy:
    def __init__(self, Name, Dict, DroppedItems):
        self.Name = Name
        self.Description = Dict["description"]
        self.MaxDamage = Dict["maxDamage"]
        self.MinDamage = Dict["minDamage"]
        self.HP = Dict["hp"]
        self.DroppedItems = DroppedItems

    def takeDamage(self, attackVal):
        self.HP = self.HP - attackVal

        if self.HP == 1:
            return "dead"
        else:
            return "alive"

    def getName(self):
        return self.Name

    def getDescription(self):
        return self.Description

    def getMaxDamage(self):
        return self.MaxDamage

    def getHP(self):
        return self.HP

    def getItems(self):
        return self.DroppedItems
