import items
import util
import world


class Player:
  def __init__(self):
    self.inventory = [items.Club(), "Loaf of bread"]
    self.x = 1
    self.y = 2
  def print_inventory(self):
    util.pretty_print_list(self.inventory)
  def most_powerful_weapon(self):
    most_powerful_weapon = None
    most_powerful_weapon_damage = 0
    for weapon in self.inventory:
      try:
        if weapon.damage > most_powerful_weapon_damage:
          most_powerful_weapon = weapon
          most_powerful_weapon_damage = weapon.damage
      except AttributeError:
        pass
    return most_powerful_weapon
  def move(self, dx, dy):
    self.x += dx
    self.y += dy
  def move_north(self):
    self.move(dx=0, dy=-1)
  def move_south(self):
    self.move(dx=0, dy=1)
  def move_east(self):
    self.move(dx=1, dy=0)
  def move_west(self):
    self.move(dx=-1, dy=0)
  def attack(self):
    best_weapon = self.most_powerful_weapon()
    tile = world.tile_at(self.x, self.y)
    monster = tile.monster
    print("You use {} against {}!".format(best_weapon.name, monster.name))
    monster.health -= best_weapon.damage
    if monster.health < 1:
      print("You have slain the {}.".format(monster.name))
    else:
      print("The {} is injured but still in the fight.".format(monster.name))
