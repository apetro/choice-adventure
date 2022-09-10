import items

class NonPlayableCharacter:
    def __str__(self):
        return self.name

class Trader(NonPlayableCharacter):
    def __init__(self):
        self.name = "Trader"
        self.gold = 100
        self.inventory = [items.CrustyBread(), items.CrustyBread(), items.CrustyBread(),
                          items.PotionOfMinorHealing(),
                          items.Dagger()]

    def trade(self, buyer, seller):
        for i, item in enumerate(seller.inventory, 1):
            print("{}: {} - {} gold".format(i, item.name, item.gold_value))
        while True:
            user_input = input("Choose an item or Q to exit.")
            if user_input in ['q', 'Q', "exit", "quit", "Quit"]:
                return
            try:
                choice = int(user_input)
                to_swap = seller.inventory[choice - 1]
                self.swap(seller, buyer, to_swap)
            except ValueError:
                print("Invalid choice.")

    def swap(self, seller, buyer, to_swap):
        if to_swap.gold_value > buyer.gold:
            print("That's too expensive.")
            return
        seller.inventory.remove(to_swap)
        buyer.inventory.append(to_swap)
        seller.gold = seller.gold + to_swap.gold_value
        buyer.gold = buyer.gold - to_swap.gold_value
        print("Traded {} for {} gold.".format(to_swap.name, to_swap.gold_value))
