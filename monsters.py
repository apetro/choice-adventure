class Monster:
  def __init__(self, name, initial_health, damage):
    self.name = name
    self.health = initial_health
    self.damage = damage
  def __str__(self):
    return self.name
  def is_alive(self):
    return self.health > 0
