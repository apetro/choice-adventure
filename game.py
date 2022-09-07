from player import Player
import world

print("Escape from the Disquieting Cavern!")

def get_player_command():
  return input("Action: ")

def play():

  player  = Player()

  while True: # play until quit

    current_map_tile = world.tile_at(player.x, player.y)
    print(current_map_tile.intro_text())

    action_input = get_player_command()

    if action_input in ['n', 'N', "north", "North"]:
      player.move_north()
    elif action_input in ['e', 'E', "east", "East"]:
      player.move_east()
    elif action_input in ['s', 'S', "south", "South"]:
      player.move_south()
    elif action_input in ['w', 'W', "west", "West"]:
      player.move_west()
    elif action_input in ['i', 'I']:
      print("Inventory: ")
      player.print_inventory()
    elif action_input in ['a', 'A', "attack", "Attack"]:
      player.attack()
    elif action_input in ['q', 'Q', "quit", "exit", "bye"]:
      print("Exiting the game.")
      exit()
    else:
      print("Error: unrecognized input.")

play()
