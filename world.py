from re import X
from tkinter import Y


class MapTile:
  def __init__(self, x, y):
    self.x = x
    self.y = y

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
    self.x = x
    self.y = y
    self.text = text
  def intro_text(self):
    return self.text


world_map = [
  [NamedTile(0,0, "NW"), NamedTile(1,0, "N"), NamedTile(2,0, "NE")],
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
