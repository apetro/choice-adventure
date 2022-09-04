print("Escape from the Disquieting Cavern!")

def get_player_command():
  return input("Action: ")

def play():
  action_input = get_player_command()

  if action_input == 'n':
    print("You go north.")
  elif action_input == 's':
    print("You go south.")
  else:
    print("Error: unrecognized input.")

play()
