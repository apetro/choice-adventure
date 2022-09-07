import random
import monsters

class MapTile:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  def modify_player(self, player):
    pass

class StartTile(MapTile):
  def intro_text(self):
    return """
    This is the starting tile.
    """

class RoadTile(MapTile):
  def intro_text(self):
    return """
    A dusty road.
    """

class VillageTile(MapTile):
  def intro_text(self):
    return """"
    A small village.
    """

class ForestTile(MapTile):
  def intro_text(self):
    return """
    A forest.
    """

class NamedTile(MapTile):
  def __init__(self, x, y, text):
    self.text = text
    super().__init__(x, y)
  def intro_text(self):
    return self.text

class RandomMonsterTile(MapTile):
  def __init__(self, x, y):
    r = random.random()
    if r < 0.05:
      self.monster = monsters.Monster(name="Gargoyle", initial_health=100, damage=10)
    elif r < 0.10:
      self.monster = monsters.Monster(name="Giant Spider", initial_health=50, damage=5)
    elif r < 0.20:
      self.monster = monsters.Monster(name="Large Spider", initial_health=20, damage=4)
    elif r < 0.40:
      self.monster = monsters.Monster(name="Sizeable Spider", initial_health=10, damage=2)
    else:
      self.monster = monsters.Monster(name="Giant Slug", initial_health=10, damage=2)
    super().__init__(x, y)
  def intro_text(self):
    if self.monster.is_alive():
      return "A {} awaits!".format(self.monster.name)
    else:
      return "There was once a {} here, but it has been defeated.".format(self.monster.name)
  def modify_player(self, player):
    if self.monster.is_alive():
      player.health -= self.monster.damage
      print("A {} inflicts {} damage. You have {} health remaining.".format(self.monster.name, self.monster.damage, player.health))



world_map = [
  [RandomMonsterTile(0,0), NamedTile(1,0, "N"), RandomMonsterTile(2,0)],
  [NamedTile(0,1, "W"), NamedTile(1,1, "Center"), NamedTile(2,1, "E")],
  [NamedTile(0,2, "SW"), NamedTile(1,2, "S"), NamedTile(2,2, "SE")]
]

def tile_at(x, y):
  if (x < 0 or y < 0):
    return None
  try:
    return world_map[y][x]
  except IndexError:
    return None
