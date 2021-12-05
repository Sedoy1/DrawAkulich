from tkinter import *
from PaintClass import Paint


def main():
    root = Tk()
    root.geometry("1370x950")
    app = Paint(root)
    root.mainloop()


if __name__ == "__main__":
    main()

