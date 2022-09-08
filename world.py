from actions import Actions, Action
import world

import random
import monsters

debug = False

class MapTile:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  def modify_player(self, player):
    pass
  def available_tile_actions(self, player):
    available_actions = Actions()

    north_of_here = world.tile_at(self.x, self.y - 1)
    east_of_here = world.tile_at(self.x + 1, self.y)
    south_of_here = world.tile_at(self.x, self.y + 1)
    west_of_here = world.tile_at(self.x - 1, self.y)

    if debug:
      print("DEBUG: North of here is {}".format(north_of_here))
      print("DEBUG: East of here is {}".format(east_of_here))
      print("DEBUG: South of here is {}".format(south_of_here))
      print("DEBUG: West of here is {}".format(west_of_here))

    if north_of_here:
      available_actions.add_action(Action(hotkey='n', name="go North", function=player.move_north))
    if east_of_here:
      available_actions.add_action(Action(hotkey='e', name="go East", function=player.move_east))
    if south_of_here:
      available_actions.add_action(Action(hotkey='s', name="go South", function=player.move_south))
    if west_of_here:
      available_actions.add_action(Action(hotkey='w', name="go West", function=player.move_west))
    return available_actions
  def __str__(self):
    return "map tile at x={} , y={}".format(self.x, self.y)

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
  def available_tile_actions(self, player):
    actions = super().available_tile_actions(player)
    if self.monster.is_alive():
      actions.add_action(action=Action(hotkey='a', name='attack', function=player.attack))
    return actions


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
