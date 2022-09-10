from actions import Actions, Action
from dice import D6
import items
import util

debug = False


class Player:
    def __init__(self, world_map):
        self.inventory = [items.Club(), items.Analgesic("Crusty bread", 5, 1)]
        self.x = 1
        self.y = 2
        self.health = 100
        self.max_health = 100
        self.world_map = world_map
        self.gold = 5

    def print_inventory(self):
        util.pretty_print_list(self.inventory)
        print("Gold: {}".format(self.gold))

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
        self.world_map.tile_at(self.x, self.y).visit()

    def move_north(self):
        print("You move north.")
        self.move(dx=0, dy=-1)

    def move_south(self):
        print("You move south.")
        self.move(dx=0, dy=1)

    def move_east(self):
        print("You move east.")
        self.move(dx=1, dy=0)


    def move_west(self):
        print("You move west.")
        self.move(dx=-1, dy=0)

    def attack(self):
        best_weapon = self.most_powerful_weapon()
        tile = self.world_map.tile_at(self.x, self.y)
        monster = tile.monster
        print("You use {} against {}!".format(best_weapon.name, monster.name))
        monster.health -= best_weapon.damage
        if monster.health < 1:
            print("You have slain the {}.".format(monster.name))
            gold_looted = D6().roll()
            self.gold = self.gold + gold_looted
            print("You looted {} gold.".format(gold_looted))
        else:
            print("The {} is injured but still in the fight.".format(monster.name))

    def heal(self):
        analgesics = [item for item in self.inventory if isinstance(item, items.Analgesic)]
        if not analgesics:
            print("You don't have any items that can heal you.")
            return
        for i, item in enumerate(analgesics, 1):
            print("Choose a healing item to consume, or Q to exit.")
            print("{}. {}".format(i, item))
        valid = False
        while not valid:
            choice = input("")
            if choice in ['q', 'Q']:
                return
            try:
                to_consume = analgesics[int(choice) - 1]
                self.health = min(100, self.health + to_consume.healing_value)
                self.inventory.remove(to_consume)
                print("Restored to {} health.".format(self.health))
                valid = True
            except (ValueError, IndexError):
                print("Invalid choice. Try again.")

    def available_player_actions(self):
        player_actions = Actions()
        if self.inventory:
            inventory_action = Action(hotkey='i', name='Inventory', function=self.print_inventory)
            player_actions.add_action(inventory_action)
        if self.health < self.max_health:
            heal_action = Action(hotkey='h', name='Heal', function=self.heal)
            player_actions.add_action(heal_action)
        return player_actions
