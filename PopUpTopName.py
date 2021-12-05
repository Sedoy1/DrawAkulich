import tkinter
import tkinter.font
from tkinter import *
from StatusesOptions import *


class PopUpTopName:
    """Всплывающее окно где надо ввести имя у вершины"""

    def __init__(self, master):
        self.window = tkinter.Toplevel(master)
        self.font = tkinter.font.Font(size=POPUP_SIZE_TEXT, family=POPUP_FAMILY_FONT)
        Label(self.window, text="Введите имя вершины", font=self.font).grid(row=0, column=0, padx=POPUP_PADX,
                                                                            pady=POPUP_PADY)

        self.nameTop = Entry(self.window, width=POPUP_BUTTON_WIDTH)
        self.nameTop.grid(row=1, column=0, padx=POPUP_PADX, pady=POPUP_PADY)

        self.buttonAccept = Button(self.window, text="Добавить вершину", command=self.__acceptName)
        self.buttonAccept.grid(row=2, column=0, padx=POPUP_PADX, pady=POPUP_PADY)

    def __acceptName(self):
        self.answer = self.nameTop.get()
        self.window.destroy()
