import unittest

import world

import collections.abc


class WorldDslTest(unittest.TestCase):

    def test_validate_dsl(self):
        just_start_tile_dsl = """
|ST|
"""
        self.assertTrue(world.validate_dsl(just_start_tile_dsl))

    def test_parse_single_cell_world(self):
        just_start_tile_dict = {"ST": world.StartTile}
        just_start_tile_dsl = """
|ST|
"""
        parsed_world = world.parse_world_dsl(dsl=just_start_tile_dsl, type_dict=just_start_tile_dict, the_world=None)
        self.assertTrue(isinstance(parsed_world, collections.abc.Sequence))
        self.assertTrue(parsed_world)
        self.assertTrue(isinstance(parsed_world[0], collections.abc.Sequence))
        self.assertTrue(parsed_world[0])
        self.assertTrue(isinstance(parsed_world[0][0], world.StartTile))

    def test_parse_3_by_3_world(self):
        realistic_tile_dict = {
            "ST": world.StartTile,
            "FO": world.ForestTile,
            "RO": world.RoadTile
        }

        realistic_dsl = """
|FO|RO|FO|
|FO|ST|RO|
|FO|RO|FO|
"""

        parsed_world = world.World(map_dsl=realistic_dsl, type_dict=realistic_tile_dict)
        self.assertTrue(parsed_world.tile_at(0, 0))
        self.assertTrue(parsed_world.tile_at(1, 1))
        self.assertTrue(parsed_world.tile_at(2, 2))

    def test_parse_dsl_to_lines(self):
        single_cell_dsl = "|ST|"
        self.assertEqual(["|ST|"], world.parse_world_dsl_to_lines(single_cell_dsl))
        another_single_cell_dsl = """
|ST|
"""
        self.assertEqual(["|ST|"], world.parse_world_dsl_to_lines(another_single_cell_dsl))

        realistic_dsl = """
|FO|RO|FO|
|FO|ST|RO|
|FO|RO|FO|
"""
        self.assertEqual(["|FO|RO|FO|", "|FO|ST|RO|", "|FO|RO|FO|"], world.parse_world_dsl_to_lines(realistic_dsl))


if __name__ == '__main__':
    unittest.main()
