from player import Player

print("Escape from the Disquieting Cavern!")

def get_player_command():
  return input("Action: ")

def play():

  player  = Player()

  while True: # play until quit
    action_input = get_player_command()

    if action_input in ['n', 'N']:
      print("You go north.")
    elif action_input in ['s', 'N']:
      print("You go south.")
    elif action_input in ['i', 'I']:
      print("Inventory: ")
      player.print_inventory()
    elif action_input in ['q', 'Q', "quit", "exit", "bye"]:
      print("Exiting the game.")
      exit()
    else:
      print("Error: unrecognized input.")

play()
