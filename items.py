class Weapon:
  def __str__(self):
    return self.name

class Rock(Weapon):
  def __init__(self):
    self.name = "Rock"
    self.description = "A fist-sized rock suitable for bludgeoning."
    self.damage = 1
    self.gold_value = 1

class Dagger(Weapon):
  def __init__(self):
    self.name = "Dagger"
    self.description = "A solid but rusty knife"
    self.damage = 3
    self.gold_value = 3

class Club(Weapon):
  def __init__(self):
    self.name = "Club"
    self.description = "A solid wooden club suitable for bludgeoning"
    self.damage = 3
    self.gold_value = 1

class Analgesic:
  def __init__(self, name, healing_value, gold_value):
    self.name = name
    self.healing_value = healing_value
    self.gold_value = gold_value
  def __str__(self):
    return "{} (+{} health)".format(self.name, self.healing_value)

class CrustyBread(Analgesic):
    def __init__(self):
        super.__init__("Crusty bread", 5, 5)

class PotionOfMinorHealing(Analgesic):
    def __init__(self):
        super.__init__("Potion of minor healing", 10, 10)

class OptionOfMajorHealing(Analgesic):
    def __init__(self):
        super.__init__("Potion of major healing", 20, 40)
