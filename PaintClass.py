import math
import tkinter.font
from tkinter import *
from tkinter import messagebox
from StatusesOptions import *
from Top import Top
from PopUpTopName import PopUpTopName


def DrawCircle(canvas, point, color=TOP_COLOR, color_outline=TOP_OUTLINE):
    canvas.create_oval(point.x - TOP_SIZE,
                       point.y - TOP_SIZE,
                       point.x + TOP_SIZE,
                       point.y + TOP_SIZE,
                       fill=color, outline=color_outline, width=TOP_WIDTH)


class Paint(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.font = tkinter.font.Font(family=STANDARD_FAMILY_FONT, size=STANDARD_SIZE_TEXT)
        self.__initText()
        self.__initButtons()
        self.__initCanvas()
        self.pack(fill=BOTH, expand=1)

        self.numberTop = 0
        self.tops = {}
        self.action = None
        self.firstTopClick = None
        self.secondTopClick = None

    def __initText(self):
        """Инициализация текста"""
        Label(self, text="Действия", font=self.font).grid(row=0, column=0, padx=STANDARD_PADX, pady=STANDARD_PADY)

        Label(self, text="Цвет № 1", font=self.font).grid(row=1, column=0, padx=STANDARD_PADX, pady=STANDARD_PADY)

        Label(self, text="Цвет № 2", font=self.font).grid(row=1, column=2, padx=STANDARD_PADX, pady=STANDARD_PADY)

    def __initCanvas(self):
        """Инициализирования поля для рисования"""
        self.parent.title("Раскраска графов")

        self.canvas = Canvas(self, bg='white', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
        self.canvas.grid(row=2, column=1, columnspan=5, sticky=E + W + S + N)
        self.canvas.bind("<Button-1>", self.CanvasClick)

    def __initButtons(self):
        """Инициализирования кнопок"""
        self.buttonAddTop = Button(self, text="Добавить вершину", command=self.__actionAddTop, font=self.font,
                                   width=STANDARD_BUTTON_WIDTH)
        self.buttonAddTop.grid(row=0, column=1, padx=STANDARD_PADX, pady=STANDARD_PADY)

        self.buttonConnectTops = Button(self, text="Соединить вершины", command=self.__actionConnectTops,
                                        font=self.font, width=STANDARD_BUTTON_WIDTH)
        self.buttonConnectTops.grid(row=0, column=2, padx=STANDARD_PADX, pady=STANDARD_PADY)

        self.buttonPaintTops = Button(self, text="Раскрасить вершины", command=self.__actionPaintTops, font=self.font,
                                      width=STANDARD_BUTTON_WIDTH)
        self.buttonPaintTops.grid(row=0, column=3, padx=STANDARD_PADX, pady=STANDARD_PADY)

        self.buttonPaintTops = Button(self, text="Удалить вершины", command=self.__actionDeleteTops, font=self.font,
                                      width=STANDARD_BUTTON_WIDTH)
        self.buttonPaintTops.grid(row=0, column=4, padx=STANDARD_PADX, pady=STANDARD_PADY)

        self.buttonDeleteAll = Button(self, text="Очистить лист", command=self.__actionClearCanvas,
                                      font=self.font,
                                      width=STANDARD_BUTTON_WIDTH)
        self.buttonDeleteAll.grid(row=0, column=5, padx=STANDARD_PADX, pady=STANDARD_PADY)

    def CanvasClick(self, position):
        """Взаимодействия с полотном"""
        save_position_x = position.x
        save_position_y = position.y
        new_top = Top(self.numberTop, save_position_x, save_position_y)
        if self.action == Status.AddTop:
            self.__countMatches(save_position_x, save_position_y)
            if self.countMatches == len(self.tops.keys()):
                popup = PopUpTopName(self)
                self.wait_window(popup.window)
                name = popup.answer
                # добавляем новую вершину
                self.tops[new_top] = []
                self.numberTop += 1
                DrawCircle(self.canvas, position)
                self.canvas.create_text(position.x, position.y, text=name)
            else:
                tkinter.messagebox.showerror(title="Ошибка", message="Данное место уже занято")

        elif self.action == Status.ConnectTops:
            self.__findMatch(save_position_x, save_position_y)
            if self.firstTopClick is None and self.foundElement is not None:
                self.firstTopClick = self.foundElement
                self.__makeTopLight()

            elif self.secondTopClick is None and self.foundElement is not None:
                self.__makeTopLight("off")
                self.secondTopClick = self.foundElement
                self.tops[self.firstTopClick].append(self.secondTopClick)
                self.tops[self.secondTopClick].append(self.firstTopClick)
                self.__drawConnectionTops()
                self.secondTopClick = None
                self.firstTopClick = None

        elif self.action == Status.DeleteTops:
            self.__findMatch(save_position_x, save_position_y)
            if self.foundElement is not None:
                DrawCircle(self.canvas, self.foundElement, color=COLOR_DELETE, color_outline=COLOR_DELETE)

                for element in self.tops[self.foundElement]:  # удаляет все исходящие пути
                    self.canvas.create_line(self.foundElement.x, self.foundElement.y, element.x, element.y,
                                            fill=COLOR_DELETE, width=LINE_WIDTH)
                    DrawCircle(self.canvas, element)

                for top in self.tops.keys():  # удаляет все входящие пути
                    if self.foundElement in self.tops[top]:
                        self.tops[top].remove(self.foundElement)

                self.tops.pop(self.foundElement)

    # Смена действия
    ################################
    def __actionAddTop(self):
        self.action = Status.AddTop

    def __actionConnectTops(self):
        self.firstTopClick = None
        self.secondTopClick = None
        self.action = Status.ConnectTops

    def __actionPaintTops(self):
        for top in self.tops.keys():
            print(self.tops)
            print(str(top) + ":", end=" ")
            for element in self.tops[top]:
                print(element)
            print("------------------")
        # TODO запустить алгоритм от сюда
        self.action = Status.Nothing

    def __actionDeleteTops(self):
        self.action = Status.DeleteTops

    def __actionClearCanvas(self):
        self.action = Status.Nothing
        self.tops.clear()
        self.canvas.delete("all")

    ##################################

    def __makeTopLight(self, status="on"):
        """Выделяет выбранную вершину"""
        if status == "on":
            DrawCircle(self.canvas, self.firstTopClick, color=TOP_COLOR_CHOICE)
        else:
            DrawCircle(self.canvas, self.firstTopClick)

    def __countMatches(self, save_position_x, save_position_y):
        """Поиск совпадений по всем точкам"""
        self.countMatches = 0
        for element in self.tops.keys():
            if math.sqrt((save_position_x - element.x) ** 2 + (save_position_y - element.y) ** 2) > TOP_SIZE and \
                    math.sqrt((save_position_x + TOP_SIZE - element.x) ** 2 + (
                            save_position_y - element.y) ** 2) > TOP_SIZE and \
                    math.sqrt((save_position_x - TOP_SIZE - element.x) ** 2 + (
                            save_position_y - element.y) ** 2) > TOP_SIZE and \
                    math.sqrt((save_position_x - element.x) ** 2 + (
                            save_position_y + TOP_SIZE - element.y) ** 2) > TOP_SIZE and \
                    math.sqrt(
                        (save_position_x - element.x) ** 2 + (save_position_y - TOP_SIZE - element.y) ** 2) > TOP_SIZE:
                self.countMatches += 1

    def __findMatch(self, save_position_x, save_position_y):
        """Поиск совпадающей точки"""
        self.foundElement = None
        for element in self.tops.keys():
            if element.x - TOP_SIZE <= save_position_x <= element.x + TOP_SIZE and \
                    element.y - TOP_SIZE <= save_position_y <= element.y + TOP_SIZE:
                self.foundElement = element
                break

    def __drawConnectionTops(self):
        """Рисует линию между точками"""
        self.canvas.create_line(self.firstTopClick.x, self.firstTopClick.y,
                                self.secondTopClick.x, self.secondTopClick.y,
                                fill=LINE_COLOR, width=LINE_WIDTH)
        DrawCircle(self.canvas, self.firstTopClick)
        DrawCircle(self.canvas, self.secondTopClick)
