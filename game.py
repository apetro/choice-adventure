print("Escape from the Disquieting Cavern!")

class Weapon:
  def __str__(self):
    return self.name

class Rock(Weapon):
  def __init__(self):
    self.name = "Rock"
    self.description = "A fist-sized rock suitable for bludgeoning."
    self.damage = 1

class Dagger(Weapon):
  def __init__(self):
    self.name = "Dagger"
    self.description = "A solid but rusty knife"
    self.damage = 3

class Club(Weapon):
  def __init__(self):
    self.name = "Club"
    self.description = "A solid wooden club suitable for bludgeoning"
    self.damage = 3

def get_player_command():
  return input("Action: ")

def play():

  inventory = [Club(), 'Load of bread']

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
