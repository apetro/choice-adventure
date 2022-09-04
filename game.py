print("Escape from the Disquieting Cavern!")

def get_player_command():
  return input("Action: ")

def play():

  inventory = ['Club', 'Load of bread']

  action_input = get_player_command()

  if action_input in ['n', 'N']:
    print("You go north.")
  elif action_input in ['s', 'N']:
    print("You go south.")
  elif action_input in ['i', 'I']:
    print("Inventory: ")
    print(inventory)
  else:
    print("Error: unrecognized input.")

play()
