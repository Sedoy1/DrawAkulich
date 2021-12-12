import StatusesOptions


class Top:
    def __init__(self, name_top, x, y, color=StatusesOptions.TOP_COLOR):
        self.index = name_top
        self.x = x
        self.y = y
        self.color = color

    def __hash__(self):
        return hash(self.index)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __str__(self):
        return "index {} x {} , y{}".format(self.index, self.x, self.y)
