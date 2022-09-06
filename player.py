import items
import util

class Player:
  def __init__(self):
    self.inventory = [items.Club(), "Loaf of bread"]
  def print_inventory(self):
    util.pretty_print_list(self.inventory)
