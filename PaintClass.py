import math
import time
import tkinter.font
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from StatusesOptions import *
from Top import Top
from ComputePoints import *


def DrawCircle(canvas, point, number, color=TOP_COLOR, color_outline=TOP_OUTLINE):
    number += 1
    canvas.create_oval(point.x - TOP_SIZE,
                       point.y - TOP_SIZE,
                       point.x + TOP_SIZE,
                       point.y + TOP_SIZE,
                       fill=color, outline=color_outline, width=TOP_WIDTH)
    canvas.create_text(point.x, point.y, text=number)


class Paint(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.font = tkinter.font.Font(family=STANDARD_FAMILY_FONT, size=STANDARD_SIZE_TEXT)
        self.frameActions = Frame(self)
        self.frameOptionsGame = Frame(self)
        self.frameFoundPaints = Frame(self)
        self.__initText()
        self.__initBoxes()
        self.__initButtons()
        self.__initCanvas()
        self.__initBinds()
        self.pack(fill=BOTH, expand=1)

        self.numberTop = 0
        self.tops = {}
        self.action = None
        self.firstTopClick = None
        self.secondTopClick = None

    def __initText(self):
        """Инициализация текста"""
        Label(self, text="Действия", font=self.font).grid(row=0, column=0, padx=STANDARD_PADX, pady=STANDARD_PADY)

        Label(self, text="Режим игры", font=self.font).grid(row=1, column=0, padx=STANDARD_PADX, pady=STANDARD_PADY)

        self.labelDemonstrate = Label(self, text="Параметры отображения", font=self.font)

        self.labelFoundedPaints = Label(self, text="Найденные раскраски", font=self.font)

    def __initBoxes(self):
        """Инициализация боксов с текстом"""
        self.boxGameRegime = Combobox(self, state='readonly', values=GAME_REGIME, font=self.font)
        self.boxGameRegime.grid(row=1, column=1, padx=STANDARD_PADX, pady=STANDARD_PADY)

        self.boxDemonstrateRegime = Combobox(self, state='readonly', values=DEMONSTRATE_REGIME, font=self.font)

        self.boxFoundPaints = Combobox(self, state='readonly', font=self.font)

    def __initCanvas(self):
        """Инициализирования поля для рисования"""
        self.parent.title("Раскраска графов")

        self.canvas = Canvas(self, bg='white', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
        self.canvas.grid(row=2, column=0, columnspan=5, sticky=E + W + S + N)
        self.canvas.bind("<Button-1>", self.CanvasClick)

    def __initButtons(self):
        """Инициализирования кнопок"""
        self.buttonAddTop = Button(self, text="Добавить вершину", command=self.__actionAddTop, font=self.font,
                                   width=STANDARD_BUTTON_WIDTH)
        self.buttonAddTop.grid(row=0, column=1, padx=STANDARD_PADX, pady=STANDARD_PADY)

        self.buttonConnectTops = Button(self, text="Соединить вершины", command=self.__actionConnectTops,
                                        font=self.font, width=STANDARD_BUTTON_WIDTH)
        self.buttonConnectTops.grid(row=0, column=2, padx=STANDARD_PADX, pady=STANDARD_PADY)

        self.buttonPaintTops = Button(self, text="Найти раскраски", command=self.__actionFindPaintings, font=self.font,
                                      width=STANDARD_BUTTON_WIDTH)
        self.buttonPaintTops.grid(row=0, column=3, padx=STANDARD_PADX, pady=STANDARD_PADY)

        self.buttonDeleteAll = Button(self, text="Очистить лист", command=self.__actionClearCanvas,
                                      font=self.font,
                                      width=STANDARD_BUTTON_WIDTH)
        self.buttonDeleteAll.grid(row=0, column=4, padx=STANDARD_PADX, pady=STANDARD_PADY)

        self.buttonPaintTops = Button(self, text="Раскрасить вершины", command=self.__actionPaintTops, font=self.font,
                                      width=STANDARD_BUTTON_WIDTH)

    def __initBinds(self):
        """Устанавливает бинды на виджеты"""
        self.boxGameRegime.bind("<<ComboboxSelected>>", self.__callbackBoxGameRegime)
        self.boxDemonstrateRegime.bind("<<ComboboxSelected>>", self.__callbackBoxDemonstrateRegime)

    def CanvasClick(self, position):
        """Взаимодействия с полотном"""
        save_position_x = position.x
        save_position_y = position.y
        new_top = Top(self.numberTop, save_position_x, save_position_y)
        if self.action == Status.AddTop:
            self.__countMatches(save_position_x, save_position_y)
            if self.countMatches == len(self.tops.keys()):
                # добавляем новую вершину
                self.tops[new_top] = []
                self.numberTop += 1
                DrawCircle(self.canvas, new_top, self.numberTop - 1)
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

    # Смена действия
    ################################
    def __actionAddTop(self):
        self.__normalizeTops()
        self.action = Status.AddTop

    def __actionConnectTops(self):
        self.__normalizeTops()
        self.firstTopClick = None
        self.secondTopClick = None
        self.action = Status.ConnectTops

    def __actionFindPaintings(self):
        """Нахождения значения раскрасок"""
        self.typeColorings = process(self.tops)
        self.labelFoundedPaints.grid(row=0, column=7, padx=STANDARD_PADX, pady=STANDARD_PADY)
        self.boxFoundPaints.grid(row=1, column=7, padx=STANDARD_PADX, pady=STANDARD_PADY)
        print(self.typeColorings)

        self.boxFoundPaints['values'] = ["Раскраска №" + str(i) for i in range(len(self.typeColorings))]
        self.boxFoundPaints.current(0)

    def __actionPaintTops(self):
        """Раскрашиваем вершины"""
        number_paint = self.boxFoundPaints.current()
        if self.boxDemonstrateRegime.get() == "Мгновенно" or self.boxDemonstrateRegime.get() == "Анимировано":
            for number_top, value in enumerate(self.typeColorings[number_paint]):
                if value == 1:
                    DrawCircle(self.canvas, list(self.tops.keys())[number_top], number_top, color=TOP_COLOR_PAINT)
                    if self.boxDemonstrateRegime.get() == "Анимировано":
                        time.sleep(ANIMATE_PAUSE)
                        self.update()
                else:
                    DrawCircle(self.canvas, list(self.tops.keys())[number_top], number_top, color=TOP_COLOR)
        self.action = Status.Nothing

    def __actionClearCanvas(self):
        self.action = Status.Nothing
        self.tops.clear()
        self.numberTop = 0
        self.canvas.delete("all")

    ##################################

    def __makeTopLight(self, status="on"):
        """Выделяет выбранную вершину"""
        if status == "on":
            DrawCircle(self.canvas, self.firstTopClick, self.firstTopClick.index, color=TOP_COLOR_CHOICE)
        else:
            DrawCircle(self.canvas, self.firstTopClick, self.firstTopClick.index)

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
        DrawCircle(self.canvas, self.firstTopClick, self.firstTopClick.index)
        DrawCircle(self.canvas, self.secondTopClick, self.secondTopClick.index)

    def __normalizeTops(self):
        """Раскрашивает все вершины в первоначальный цвет"""
        for top in self.tops.keys():
            DrawCircle(self.canvas, top, top.index)

    def __callbackBoxGameRegime(self, event):
        """Коллбек на комбобокс с гейм режимом"""
        value = self.boxGameRegime.get()
        if value == "Демонстрация":
            # иницализация интерфейса демонстрации
            self.labelDemonstrate.grid(row=1, column=2, padx=STANDARD_PADX, pady=STANDARD_PADY)
            self.boxDemonstrateRegime.grid(row=1, column=3, padx=STANDARD_PADX, pady=STANDARD_PADY)
        self.__actionClearCanvas()

    def __callbackBoxDemonstrateRegime(self, event):
        """Коллбек на выбор режима демонстрации"""
        self.buttonPaintTops.grid(row=1, column=4, padx=STANDARD_PADX, pady=STANDARD_PADY)
        self.__normalizeTops()
