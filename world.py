from actions import Actions, Action

import names
import npc
import random
import monsters

debug = False


class MapTile:
    def __init__(self, x, y, the_world):
        self.x = x
        self.y = y
        self.the_world = the_world

    def modify_player(self, player):
        pass

    def available_tile_actions(self, player):
        available_actions = Actions()

        north_of_here = self.the_world.tile_at(self.x, self.y - 1)
        east_of_here = self.the_world.tile_at(self.x + 1, self.y)
        south_of_here = self.the_world.tile_at(self.x, self.y + 1)
        west_of_here = self.the_world.tile_at(self.x - 1, self.y)

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

    def __init__(self, x, y, the_world):
        super().__init__(x, y, the_world)
        self.trader = npc.Trader()
        self.village_name = names.generate_village_name()

    def __str__(self):
        return self.village_name + " village"

    def intro_text(self):
        return """
        The small village of {}. A trader has set up a cart with wares in the village square.
        """.format(self.village_name)

    def available_tile_actions(self, player):
        self.player = player
        buy_action = Action(hotkey='b', name="Buy from trader", function=self.buy)
        sell_action = Action(hotkey='t', name="sell to Trader", function=self.sell)

        actions = super().available_tile_actions(player)

        actions.add_action(buy_action)
        actions.add_action(sell_action)
        return actions

    def buy(self):
        self.trader.trade(self.player, self.trader)
    def sell(self):
        self.trader.trade(self.trader, self.player)


class ForestTile(MapTile):
    def intro_text(self):
        return """
        A forest.
        """

class RandomMonsterTile(MapTile):
    def __init__(self, x, y, the_world):
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
        super().__init__(x, y, the_world)

    def intro_text(self):
        if self.monster.is_alive():
            return "A {} awaits!".format(self.monster.name)
        else:
            return "There was once a {} here, but it has been defeated.".format(self.monster.name)

    def modify_player(self, player):
        if self.monster.is_alive():
            player.health -= self.monster.damage
            print("A {} inflicts {} damage. You have {} health remaining.".format(self.monster.name, self.monster.damage,
                                                                            player.health))

    def available_tile_actions(self, player):
        actions = super().available_tile_actions(player)
        if self.monster.is_alive():
            actions.add_action(action=Action(hotkey='a', name='attack', function=player.attack))
        return actions


world_map_dsl = """
|RM|VI|RM|FO|FO|FO|VI|FO|
|FO|RD|FO|FO|RD|RD|RD|FO|
|RD|ST|RD|RD|RD|FO|FO|FO|
|VI|RD|RM|RD|FO|RM|RM|RM|
|RD|FO|FO|FO|FO|FO|FO|FO|
|RD|FO|FO|FO|FO|FO|FO|FO|
|RD|RD|RD|RD|FO|FO|FO|FO|
|FO|FO|FO|RD|FO|FO|FO|FO|
"""

tile_type_dict = {
    "ST": StartTile,
    "RD": RoadTile,
    "FO": ForestTile,
    "VI": VillageTile,
    "RM": RandomMonsterTile,
    "  ": None
}


def parse_world_dsl(dsl, type_dict, the_world):
    world_map = []
    if not validate_dsl(dsl):
        raise SyntaxError("World DSL is not valid.")
    dsl_lines = parse_world_dsl_to_lines(dsl)
    for y, dsl_row in enumerate(dsl_lines):
        row = parse_world_dsl_row(dsl_row=dsl_row, type_dict=type_dict, y=y, the_world=the_world)
        world_map.append(row)
    return world_map

def parse_world_dsl_to_lines(dsl):
    """Given a world DSL, splits it to an array of meaningful lines"""
    dsl_lines = dsl.splitlines()
    dsl_lines = [line for line in dsl_lines if line]
    return dsl_lines


def parse_world_dsl_row(dsl_row, type_dict, y, the_world):
    """Parse a single row of the world DSL.
    """
    row = []
    dsl_cells = dsl_row.split('|')
    dsl_cells = [cell for cell in dsl_cells if cell]
    for x, dsl_cell in enumerate(dsl_cells):
        tile_type = type_dict[dsl_cell]
        row.append(tile_type(x, y, the_world) if tile_type else None)
    return row


def validate_dsl(dsl):
    if dsl.count("|ST|") != 1:
        return False  # there should be exactly one start tile
    lines = dsl.splitlines()
    lines = [l for l in lines if l]
    pipe_counts = [line.count('|') for line in lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False  # all lines should have the same number of pipes and thus cells
    return True


class World:

    def __init__(self, map_dsl, type_dict):
        self.tile_grid = parse_world_dsl(dsl=map_dsl, type_dict=type_dict, the_world=self)
        if debug:
            print("Inited world as {}".format(self.__str__()))

    def tile_at(self, x, y):
        if debug:
            print("DEBUG: tile_at({},{})".format(x, y))
        if (x < 0 or y < 0):
            return None
        try:
            return self.tile_grid[y][x]
        except IndexError:
            return None

    def __str__(self):
        string_representation = "world: ["
        if self.tile_grid:
            for row in self.tile_grid:
                string_representation = string_representation + "["
                for tile in row:
                    string_representation = string_representation + str(tile) + '|'
                string_representation = string_representation + "]"
        return string_representation
