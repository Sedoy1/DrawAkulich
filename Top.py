class Top:
    def __init__(self, name_top, x, y):
        self.index = name_top
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __str__(self):
        return "index {} x {} , y{}".format(self.index, self.x, self.y)
