import random

trees = ["Maple", "Oak", "Willow"]
tree_parts = ["bark", "branch", "leaf", "root"]

def generate_village_name():
    return "{}{}".format(random.choice(trees), random.choice(tree_parts))
