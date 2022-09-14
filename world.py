import herbalism
from actions import Actions, Action, ForageAction

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
        self.known = False

    def visit(self):
        self.known = True
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
            if north_of_here.known:
                available_actions.add_action(
                    Action(name="go North to {}".format(north_of_here), function=player.move_north))
            else:
                available_actions.add_action(Action(name="go North", function=player.move_north))
        if east_of_here:
            if east_of_here.known:
                available_actions.add_action(
                    Action(name="go East to {}".format(east_of_here), function=player.move_east))
            else:
                available_actions.add_action(Action(name="go East", function=player.move_east))
        if south_of_here:
            if south_of_here.known:
                available_actions.add_action(
                    Action(name="go South to {}".format(south_of_here), function=player.move_south))
            else:
                available_actions.add_action(Action(name="go South", function=player.move_south))
        if west_of_here:
            if west_of_here.known:
                available_actions.add_action(
                    Action(name="go West to {}".format(west_of_here), function=player.move_west))
            else:
                available_actions.add_action(Action(name="go West", function=player.move_west))
        return available_actions

    def __str__(self):
        return "map tile at x={} , y={}".format(self.x, self.y)

    def two_letter_code(self):
        return "??"


class StartTile(MapTile):
    def intro_text(self):
        return """
        This is the starting tile.
        """

    def __str__(self):
        return "Home"

    def two_letter_code(self):
        return "ST"


class RoadTile(MapTile):
    def intro_text(self):
        return """
        A dusty road.
        """

    def __str__(self):
        return "dusty road"

    def visit(self):
        super().visit()
        for adjacent_tile in self.the_world.tiles_adjacent_to(self):
            adjacent_tile.visit()

    def two_letter_code(self):
        return "RO"


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
        buy_action = Action(name="Buy from trader", function=self.buy)
        sell_action = Action(name="sell to Trader", function=self.sell)

        actions = super().available_tile_actions(player)

        actions.add_action(buy_action)
        actions.add_action(sell_action)
        return actions

    def buy(self):
        self.trader.trade(self.player, self.trader)

    def sell(self):
        self.trader.trade(self.trader, self.player)

    def two_letter_code(self):
        return "VI"

class ForestTile(MapTile):
    def intro_text(self):
        return """
        A forest.
        """

    def __str__(self):
        return "forest"

    def available_tile_actions(self, player):
        actions = super().available_tile_actions(player)
        actions.add_action(ForageAction(herbalism.DruidLeaf(), player))
        return actions

    def two_letter_code(self):
        return "FO"


class RandomMonsterTile(MapTile):
    def __init__(self, x, y, the_world):
        r = random.random()
        if r < 0.05:
            self.monster = monsters.Gargoyle()
        elif r < 0.10:
            self.monster = monsters.GiantSpider()
        elif r < 0.20:
            self.monster = monsters.LargeSpider()
        elif r < 0.40:
            self.monster = monsters.SizeableSpider()
        else:
            self.monster = monsters.GiantSlug()
        super().__init__(x, y, the_world)

    def __str__(self):
        return "monster"

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
            actions.add_action(action=Action(name='attack', function=player.attack))
        return actions

    def two_letter_code(self):
        return "RM"

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

    def tile_at(self, x, y):
        if debug:
            print("DEBUG: tile_at({},{})".format(x, y))
        if (x < 0 or y < 0):
            return None
        try:
            return self.tile_grid[y][x]
        except IndexError:
            return None

    def tiles_adjacent_to(self, some_tile):
        adjacent_tiles = []
        if not some_tile:
            return adjacent_tiles

        tile_to_north = self.tile_at(some_tile.x, some_tile.y - 1)
        tile_to_east = self.tile_at(some_tile.x + 1, some_tile.y)
        tile_to_south = self.tile_at(some_tile.x, some_tile.y + 1)
        tile_to_west = self.tile_at(some_tile.x - 1, some_tile.y)

        if tile_to_north:
            adjacent_tiles.append(tile_to_north)
        if tile_to_east:
            adjacent_tiles.append(tile_to_east)
        if tile_to_south:
            adjacent_tiles.append(tile_to_south)
        if tile_to_west:
            adjacent_tiles.append(tile_to_west)

        return adjacent_tiles

    def __str__(self):
        string_representation = "world:\n"
        if self.tile_grid:
            for row in self.tile_grid:
                string_representation = string_representation + "|"
                for tile in row:
                    if tile:
                        string_representation = string_representation + tile.two_letter_code() + '|'
                    else:
                        string_representation = string_representation + "  " + '|'
                string_representation = string_representation + "\n"
        return string_representation

class RandomWorld(World):
    def __init__(self, size=10):
        self.tile_grid = []

        for y in range(0, size):
            row = []
            for x in range(0, size):
                row.append(None)
            self.tile_grid.append(row)

        print(self.__str__())


        # choose coordinates for the first village

        random.choice

        village_y_s = []
        for i in range(round(size / 4)):
            candidate_y = random.choice(range(0, round((size - 1) / 2)))
            if candidate_y not in village_y_s \
                    and (candidate_y - 1) not in village_y_s \
                    and (candidate_y + 1) not in village_y_s:

                village_y_s.append(candidate_y)

        for y in village_y_s:
            self.add_village_pair(y, size)

        print("After adding villages.")
        print(self.__str__())

        print("Drawing roads northward from villages.")
        self.draw_roads_north_south_from_villages(size)

        print("After drawing northward roads.")
        print(self.__str__())

        print("Filling in the rest with forest.")

        for y in range(0, size):
            for x in range(0, size):
                if not self.tile_at(x, y):
                    self.tile_grid[y][x] = ForestTile(x, y, self)

        print(self.__str__())

    def add_village_pair(self, y, size):
        village_1_x = random.randint(0, round(size / 3))
        print("Placing first village at {},{}".format(village_1_x, y))

        self.tile_grid[y][village_1_x] = VillageTile(village_1_x, y, self)

        print(self.__str__())

        # the second village will be due west of the first

        village_2_x = random.randint(round(size / 2), size - 1)

        print("Placing second village at {},{}.".format(village_2_x, y))

        self.tile_grid[y][village_2_x] = VillageTile(village_2_x, y, self)

        print(self.__str__())

        print("The distance between the villages is {}.".format(village_2_x - village_1_x))

        if y == 0 or y == size - 1 or village_2_x - village_1_x < 12 or  random.random() < 0.1:
            # connect the two with road in a straight line
            print("Adding straight road between the villages")

            self.connect_east_west_with_road(village_1_x + 1, village_2_x, y)
            print(self.__str__())
        else:
            # connect with a road that displaces one tile north or south
            print("Connecting the villages with a road with a wiggle.")
            displace_x_1 = random.choice(range(village_1_x + 2, round(village_2_x - village_1_x / 3) + village_1_x))
            displace_x_2 = random.choice(
                range(village_1_x + round(2 * (village_2_x - village_1_x) /  3), village_2_x - 2))

            self.connect_east_west_with_road(village_1_x + 1, displace_x_1, y)

            y_mod = random.choice([-1, 1])

            self.connect_east_west_with_road(displace_x_1 - 1, displace_x_2, y + y_mod)

            self.connect_east_west_with_road(displace_x_2 - 1, village_2_x, y)


            print(self.__str__())

    def add_road_if_empty(self, x, y):
        existing_tile = self.tile_at(x, y)
        if existing_tile:
            print("Did not add road at {}, {} because tile already there: {}.".format(x, y, existing_tile))
        else:
            self.tile_grid[y][x] = RoadTile(x, y, self)

    def draw_roads_north_south_from_villages(self, size):
        for x in range(0, size):
            for y in range(1, size): # No need to draw roads north from villages in top row
                tile_there = self.tile_at(x, y)
                if tile_there and tile_there.two_letter_code() == "VI":
                    print("Drawing road north from {}, {}.".format(x, y))
                    self.draw_road_north_from(x, y - 1)
                    print(self.__str__())

    def draw_road_north_from(self, start_x, start_y):
        x = start_x
        for y in range(start_y, 0, -1):
            tile_to_east = self.tile_at(x + 1, y)
            tile_to_northeast = self.tile_at(x + 1, y - 1)
            tile_to_southeast = self.tile_at(x + 1, y + 1)
            tile_to_west = self.tile_at(x - 1, y)
            tile_to_northwest = self.tile_at(x - 1, y -1)
            tile_to_southwest = self.tile_at(x - 1, y + 1)
            if tile_to_east and tile_to_east.two_letter_code() == "RO" \
                    and tile_to_northeast and tile_to_northeast.two_letter_code() == "RO" \
                    and tile_to_southeast and tile_to_southeast.two_letter_code() == "RO":
                print("Stopping northward road at {}. {} because detected adjacent to parallel road to east.".format(x, y))
                return # do not draw roads parallel to immediately adjacent roads
            if tile_to_west and tile_to_west.two_letter_code() == "RO" \
                    and tile_to_northwest and tile_to_northwest.two_letter_code() == "RO" \
                    and tile_to_southwest and tile_to_southwest.two_letter_code() == "RO":
                print("Stopping northward road at {}, {} because detected adjacent to parallel road to west.".format(x, y))
                return  # do not draw roads parallel to immediately adjacent roads
            if random.random() < (start_y - y) / 100: # roads more likely to end prematurely the longer they go
                return
            self.add_road_if_empty(x, y)

    def connect_east_west_with_road(self, x1, x2, y):
        for x in range(x1, x2):
            tile_to_north = self.tile_at(x, y - 1)
            tile_to_northeast = self.tile_at(x + 1, y - 1)
            tile_to_northwest = self.tile_at(x - 1, y - 1)
            tile_to_south = self.tile_at(x, y + 1)
            tile_to_southeast = self.tile_at(x + 1, y + 1)
            tile_to_southwest = self.tile_at(x - 1, y + 1)

            if tile_to_north and tile_to_north.two_letter_code() == "RO" \
                    and tile_to_northeast and tile_to_northeast.two_letter_code() == "RO" \
                    and tile_to_northwest and tile_to_northwest.two_letter_code() == "RO":
                print("Ended eastward road at {}, {} because detected adjacent to parallel east-west road.".format(x, y))
                return
            if tile_to_south and tile_to_south.two_letter_code() == "RO" \
                and tile_to_southeast and tile_to_southeast.two_letter_code() == "RO" \
                and tile_to_southwest and tile_to_southwest.two_letter_code() == "RO":
                print(
                    "Ended eastward road at {}, {} because detected adjacent to parallel east-west road.".format(x, y))
                return

            self.add_road_if_empty(x, y)



class DsLWorld(World):

    def __init__(self, map_dsl, type_dict):
        self.tile_grid = parse_world_dsl(dsl=map_dsl, type_dict=type_dict, the_world=self)
        if debug:
            print("Inited world as {}".format(self.__str__()))


