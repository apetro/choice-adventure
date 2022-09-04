print("Escape from the Disquieting Cavern!")

def get_player_command():
  return input("Action: ")

def play():

  inventory = ['Club', 'Load of bread']

  action_input = get_player_command()

  if action_input == 'n':
    print("You go north.")
  elif action_input == 's':
    print("You go south.")
  elif action_input == 'i':
    print("Inventory: ")
    print(inventory)
  else:
    print("Error: unrecognized input.")

play()
