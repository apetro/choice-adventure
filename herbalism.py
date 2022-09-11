class Herb:
    def __init__(self):
        self.gold_value = 1
        self.name = "generic herb"
    def __str__(self):
        return self.name

class FrogRoot(Herb):
    """
    A cheap, basic herb. With druid leaf, an ingredient to make a minor healing potion.
    """
    def __init__(self):
        super().__init__()
        self.name = "frog root"

class DruidLeaf(Herb):
    """
    Another cheap, basic herb. With Frog root, an ingredient to make a minor healing potion.
    """
    def __init__(self):
        super().__init__()
        self.name = "druid leaf"

