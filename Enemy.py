import Item

class Enemy:
    Name = ""
    Description = ""
    DescriptionDict = {"Placeholder1": "Your basic grunt. Nothing to worry about",
                       "Placeholder2": "Having fed on the other creatures for years now, this one packs a punch."}
    MaxDamage = 0
    DroppedItem = Item()
    HP = 100

    def __init__(self, Name, MaxDamage, DroppedItem):
        self.Name = Name
        self.Description = self.DescriptionDict[Name]
        self.MaxDamage = MaxDamage
        self.DroppedItem = DroppedItem

    def takeDamage(self, attackVal):
        self.HP = self.HP - attackVal
        