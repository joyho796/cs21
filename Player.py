##########################################################################
# Class: Player
# Used to keep track of player stats, inventory, and location.
##########################################################################

class Player:
    def __init__(self, username):
        self.username = username
        self.room = 0
        self.hp = 100
        self.weapons = ["Knife"]
        self.potions = []
        self.currentWeapon = "Knife"


    # add a weapon to inventory
    def addWeapon(self, weaponName):
        self.weapons.append(weaponName)

    # remove item from inventory
    def removeItem(self, item):
        if item in self.weapons:
            if self.currentWeapon == item:
                self.currentWeapon = "Fist"
            self.weapons.remove(item)
        elif item in self.potions:
            self.potions.remove(item)

    # add potion to inventory
    def addPotion(self, potionName):
        self.potions.append(potionName)

    # subtrack given damage amount from hp. Returns whether the player is
    # dead or alive as a result.
    def takeDamage(self, amount):
        self.hp = self.hp - amount

        if self.hp < 1:
            return "dead"
        else:
            return "alive"

    # gain a given amount of hp
    def heal(self, amount):
        self.hp = self.hp + amount

    # get the player's current location in the dungeon.
    def getRoomNumber(self):
        return self.room

    # returns the players current inventory
    def getInventory(self):
        weaponsList = "Weapons: "
        potionsList = "Potions: "

        if len(self.weapons) == 0:
            weaponsList += "None"
        else:
            weaponsList += ", ".join(self.weapons)

        if len(self.potions) == 0:
            potionsList += "None"
        else:
            potionsList += ", ".join(self.potions)

        return weaponsList + ". " + potionsList
