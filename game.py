import items

print("Escape from the Disquieting Cavern!")

def get_player_command():
  return input("Action: ")

def play():

  inventory = [items.Club(), 'Load of bread']

  while True: # play until quit
    action_input = get_player_command()

    if action_input in ['n', 'N']:
      print("You go north.")
    elif action_input in ['s', 'N']:
      print("You go south.")
    elif action_input in ['i', 'I']:
      print("Inventory: ")
      pretty_print_list(inventory)
    else:
      print("Error: unrecognized input.")

def pretty_print_list(some_list):
  print()
  for item in some_list:
    print("* " + str(item))
  print()

play()
