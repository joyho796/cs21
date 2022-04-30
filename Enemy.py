##########################################################################
# Class: Enemy
# Used to keep track of enemy stats and inventory
##########################################################################

class Enemy:
    def __init__(self, Name, Dict, DroppedItems):
        self.Name = Name
        self.Description = Dict["description"]
        self.MaxDamage = Dict["maxDamage"]
        self.MinDamage = Dict["minDamage"]
        self.HP = Dict["hp"]
        self.DroppedItems = DroppedItems

    # subtrack given damage amount from hp. Returns whether the player is
    # dead or alive as a result.
    def takeDamage(self, attackVal):
        self.HP = self.HP - attackVal

        if self.HP < 1:
            return "dead"
        else:
            return "alive"

    # return name
    def getName(self):
        return self.Name

    # return description
    def getDescription(self):
        return self.Description

    # return max damage
    def getMaxDamage(self):
        return self.MaxDamage

    # return hp
    def getHP(self):
        return self.HP

    # return list of items
    def getItems(self):
        return self.DroppedItems
