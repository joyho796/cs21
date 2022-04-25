class Item:
    Name = ""
    Description = ""
    DescriptionDict = {
        "Sword": "An ordinary sword. Though it's been long since its glory days, the blade remains sharp.",
        "Dagger": "An assassins dagger. Chips have begun to form along its edge, but it remains a trusty tool.",
        "Potion": "A healing potion. It says healing on the red bottle, so it should be fine, right?"}
    isWeapon = False
    isWeaponDict = {
        "Sword": True,
        "Dagger": True,
        "Potion": False
    }
    MaxDamage = 0
    DamageDict = {
        "Sword": 15,
        "Dagger": 10,
        "Potion": 0
    }

    def __init__(self, Name):
        self.Name = Name
        self.Description = self.DescriptionDict[Name]
        self.isWeapon = self.isWeaponDict[Name]
        self.MaxDamage = self.DamageDict[Name]

    def getName(self):
        return self.Name

    def getDescription(self):
        return self.Description

    def getMaxDamage(self):
        return self.MaxDamage

    def getDescription(self, itemName):
        return DescriptionDict[itemName]

    def getDamage(itemName):
        return DamageDict[itemName]
