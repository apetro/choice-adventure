class Weapon:
  def __str__(self):
    return self.name

class Rock(Weapon):
  def __init__(self):
    self.name = "Rock"
    self.description = "A fist-sized rock suitable for bludgeoning."
    self.damage = 1

class Dagger(Weapon):
  def __init__(self):
    self.name = "Dagger"
    self.description = "A solid but rusty knife"
    self.damage = 3

class Club(Weapon):
  def __init__(self):
    self.name = "Club"
    self.description = "A solid wooden club suitable for bludgeoning"
    self.damage = 3
