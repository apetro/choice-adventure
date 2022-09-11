from collections import OrderedDict

debug = False


class Actions:

    def __init__(self):

        self.actions = []

    def add_action(self, action):
        self.actions.append(action)
        if debug:
             print("DEBUG: added action {}".format(action))


    def add_actions(self, actions):
        for action in actions.actions:
            self.add_action(action)

    def print_action_menu(self):
        print("Available actions:")
        for i, action in enumerate(self.actions, 1):
            print("{}: {}".format(i, action.name))
        print()

    def choose_action(self):
        chosen_action = None

        while not chosen_action:
            self.print_action_menu()
            action_input = input("Action: ")
            try:
                action_int = int(action_input)
                chosen_action = self.actions[action_int - 1]
                if chosen_action:
                    chosen_action.perform()
                else:
                    print("Error: {} is not the hotkey of an available action.".format(action_input))
            except ValueError:
                print("Error: {} is not the hotkey of an available action.".format(action_input))

    def __str__(self):
        string_representation = ""
        for hotkey in self.actions:
            string_representation = string_representation + hotkey
        return string_representation


class Action:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def __str__(self):
        return self.name

    def perform(self):
        self.function()


class ForageAction(Action):
    def __init__(self, item, player):
        super().__init__("Forage", None)
        self.effect = player.build_gain_inventory_effect(item)
        self.item_name = str(item)

    def perform(self):
        print("You forage and, luckily, find {}.".format(self.item_name))
        self.effect.apply()


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

    available_actions.add_action(Action("Quit", exit))

    return available_actions
