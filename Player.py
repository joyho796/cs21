class Player:
    def __init__(self, username):
        self.username = username
        self.room = 0
        self.hp = 100
        self.weapons = ["Knife"]
        self.potions = []
        self.currentWeapon = "Knife"


    def addWeapon(self, weaponName):
        self.weapons.append(weaponName)

    def addPotion(self, potionName):
        self.potions.append(potionName)
   
    def takeDamage(self, amount):
        self.hp = self.hp - amount

    def heal(self, amount):
        self.hp = self.hp + amount

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
