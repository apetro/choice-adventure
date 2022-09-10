import random

class Die:
    def __init__(self, sides):
        self.sides = sides

    def __str__(self):
        return "d" + str(self.sides)

    def roll(self):
        return random.randint(1, self.sides)


class D6(Die):
    def __init__(self):
        super().__init__(6)


class D20(Die):
    def __init__(self):
        super().__init__(20)


class Dice:
    def __init__(self):
        dice = []
        self.modifier = 0

    def __str__(self):
        string_representation = ""
        for die in self.dice:
            string_representation = string_representation + str(die) + " "
        if self.modifier:
            string_representation = string_representation + "+" + str(self.modifier)
        return string_representation

    def roll(self):
        total = 0
        for die in self.dice:
            total = total + die
        total = total + self.modifier
        total = min(total, 1)
        return total

    def add_die(self, die):
        self.dice.append(die)
