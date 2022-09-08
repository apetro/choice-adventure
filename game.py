from actions import Action, Actions, gather_actions
from player import Player
import world

debug = False

print("Escape from the Disquieting Cavern!")

def play():

  player  = Player()

  while True: # play until quit

    current_map_tile = world.tile_at(player.x, player.y)
    print(current_map_tile.intro_text())
    if debug:
      print("DEBUG: you are at map location x={} and y={}".format(player.x, player.y))

    current_map_tile.modify_player(player)

    available_actions = gather_actions(tile=current_map_tile, player=player)
    available_actions.choose_action()
    available_actions = None

play()
