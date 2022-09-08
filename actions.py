from collections import OrderedDict

debug = False

class Actions:

  def __init__(self):

    self.actions = OrderedDict()

  def add_action(self, action):
    self.actions[action.hotkey.lower()] = action
    if debug:
      print("DEBUG: added action {}".format(action))

  def add_actions(self, actions):
    self.actions = self.actions | actions.actions

  def action_for_key(self, hotkey):
    return self.actions.get(hotkey.lower())

  def print_action_menu(self):
    print("Available actions:")
    for action in self.actions.values():
      action.print_action()
    print()

  def choose_action(self):
    chosen_action = None

    while not chosen_action:
      self.print_action_menu()
      action_input = input("Action: ")
      chosen_action = self.actions.get(action_input)
      if chosen_action:
        chosen_action.function()
      else:
        print("Error: {} is not the hotkey of an available action.".format(action_input))

  def __str__(self):
    string_representation = ""
    for hotkey in self.actions:
      string_representation = string_representation + hotkey
    return string_representation


class Action:
  def __init__(self, hotkey, name, function):
    self.hotkey = hotkey
    self.name = name
    self.function = function
  def print_action(self):
    print(" {}: {}".format(self.hotkey, self.name))
  def __str__(self):
    return self.hotkey

def gather_actions(tile, player):

  player_actions = player.available_player_actions()

  if debug:
    print("DEBUG: from player gathered actions {}".format(player_actions))

  location_actions = tile.available_tile_actions(player)

  if debug:
    print("DEBUG: from location {} gathered actions {}".format(tile, location_actions))

  available_actions = Actions()
  available_actions.add_actions(player_actions)
  available_actions.add_actions(location_actions)

  available_actions.add_action(Action('q', "Quit", exit))

  return available_actions
