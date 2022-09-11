class Monster:
  def __init__(self, name, initial_health, damage):
    self.name = name
    self.health = initial_health
    self.damage = damage
  def __str__(self):
    return self.name
  def is_alive(self):
    return self.health > 0


class GiantSlug(Monster):
    def __init__(self):
        super().__init__("Giant slug", 5, 2)


class SizeableSpider(Monster):
    def __init__(self):
        super().__init__("Sizeable spider", 10, 4)


class LargeSpider(Monster):
    def __init__(self):
        super().__init__("Large spider", 20, 5)


class GiantSpider(Monster):
    def __init__(self):
        super().__init__("Giant Spider", 50, 8)


class Gargoyle(Monster):
    def __init__(self):
        super().__init__("Gargoyle", 100, 10)

