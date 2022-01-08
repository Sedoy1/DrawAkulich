import math
import time
import tkinter.font
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from StatusesOptions import *
from Top import Top
import copy
from ComputePoints import *


def GenerateGraph():
    return generate_random_graph()


def DrawCircle(canvas, point, number, color=TOP_COLOR, color_outline=TOP_OUTLINE):
    number += 1
    canvas.create_oval(point.x - TOP_SIZE,
                       point.y - TOP_SIZE,
                       point.x + TOP_SIZE,
                       point.y + TOP_SIZE,
                       fill=color, outline=color_outline, width=TOP_WIDTH)
    canvas.create_text(point.x, point.y, text=number)


def ClearFrame(frame):
    """Очищает выбранную рамку"""
    for widgets in frame.winfo_children():
        widgets.destroy()


class Paint(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.font = tkinter.font.Font(family=STANDARD_FAMILY_FONT, size=STANDARD_SIZE)
        self.fontStep = tkinter.font.Font(family=STEPS_FAMILY_FONT, size=STEPS_FAMILY_SIZE)
        self.frameLeft = Frame(self)
        self.frameRight = Frame(self)
        self.frameMainWidgets = Frame(self.frameLeft)
        self.frameMethodCreateGraph = Frame(self.frameLeft)
        self.frameCreateBySelf = Frame(self.frameMethodCreateGraph)
        self.frameGenerateGraph = Frame(self.frameMethodCreateGraph)
        self.frameOptionsGame = Frame(self.frameRight)
        self.frameStepByStep = LabelFrame(self.frameRight, text="Шаги для раскраски")
        self.frameCanvas = Frame(self.frameLeft)
        self.frameFoundPaints = Frame(self.frameRight)
        self.frameSolveColorings = Frame(self.frameRight)
        self.__initText()
        self.__initBoxes()
        self.__initButtons()
        self.__initCanvas()
        self.__initBinds()
        self.frameCanvas.pack(side=BOTTOM)
        self.frameOptionsGame.pack(pady=STANDARD_PADY_FRAMES)
        self.frameMethodCreateGraph.pack(side=BOTTOM)
        self.frameMainWidgets.pack(side=TOP)
        self.frameLeft.pack(side=LEFT)
        self.frameRight.pack(side=RIGHT, anchor=N)
        self.pack(fill=BOTH, expand=1)

        self.userActions = []
        self.topsPainted = []
        self.tops2PaintIndex = []
        self.currentIndexColoring = None
        self.numberTop = 0
        self.tops = {}
        self.action = None
        self.firstTopClick = None
        self.secondTopClick = None

    def __initText(self):
        """Инициализация текста"""
        Label(self.frameMainWidgets, text="Метод создания фигуры", font=self.font).pack(side=LEFT)
        Label(self.frameOptionsGame, text="Режим игры", font=self.font).pack()

        Label(self.frameOptionsGame, text="Параметры отображения", font=self.font).pack()

        Label(self.frameFoundPaints, text="Найденные раскраски", font=self.font).pack()

    def __initBoxes(self):
        """Инициализация боксов с текстом"""

        self.boxCreateRegime = Combobox(self.frameMainWidgets, state='readonly', values=GRAPH_CONSTRUCTOR_REGIME,
                                        font=self.font)
        self.boxCreateRegime.pack(side=LEFT)

        self.boxGameRegime = Combobox(self.frameOptionsGame, state='disabled', values=GAME_REGIME, font=self.font)
        self.boxGameRegime.pack()

        self.boxTypeGameRegime = Combobox(self.frameOptionsGame, state='disabled',
                                          font=self.font)

        self.boxFoundPaints = Combobox(self.frameFoundPaints, state='readonly', font=self.font)
        self.boxFoundPaints.pack()

    def __initCanvas(self):
        """Инициализирования поля для рисования"""
        self.parent.title("Раскраска графов")

        self.canvas = Canvas(self.frameCanvas, bg='white', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
        self.canvas.pack(side=BOTTOM)

    def __initButtons(self):
        """Инициализирования кнопок"""
        Button(self.frameCreateBySelf, text="Добавить вершину", command=self.__actionAddTop, font=self.font,
               width=STANDARD_BUTTON_WIDTH).pack(side=LEFT)

        Button(self.frameCreateBySelf, text="Соединить вершины", command=self.__actionConnectTops,
               font=self.font, width=STANDARD_BUTTON_WIDTH).pack(side=LEFT)

        Button(self.frameCreateBySelf, text="Найти раскраски", command=self.__findColorings, font=self.font,
               width=STANDARD_BUTTON_WIDTH).pack(side=LEFT)

        Button(self.frameMainWidgets, text="Очистить лист", command=self.__actionClearCanvas,
               font=self.font,
               width=STANDARD_BUTTON_WIDTH).pack(side=LEFT)

        Button(self.frameFoundPaints, text="Получить раскраску", command=self.__actionGetPaint, font=self.font,
               width=STANDARD_BUTTON_WIDTH).pack()

        Button(self.frameGenerateGraph, text="Сгенерировать фигуру", command=self.__generateGraph,
               font=self.font).pack()

        Button(self.frameSolveColorings, text="Проверить решение", command=self.__checkSolution, font=self.font).pack(
            pady=STANDARD_PADY)

        # Button(self.frameSolveColorings, text="Получить решение", command=self.__getSolution, font=self.font).pack(pady=STANDARD_PADY)

        self.buttonReverse = Button(self.frameRight, text="Отмена действия", command=self.__revertAction,
                                    font=self.font)

    def __initBinds(self):
        """Устанавливает бинды на виджеты"""
        self.boxGameRegime.bind("<<ComboboxSelected>>", self.__callbackBoxGameRegime)
        self.boxTypeGameRegime.bind("<<ComboboxSelected>>", self.__callbackBoxTypeGameRegime)
        self.boxFoundPaints.bind("<<ComboboxSelected>>", self.__callbackBoxFoundPaints)
        self.boxCreateRegime.bind("<<ComboboxSelected>>", self.__callbackBoxCreateRegime)
        self.canvas.bind("<Button-1>", self.CanvasClick)

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
                self.__changeColorTop(TOP_COLOR_CHOICE)

            elif self.secondTopClick is None and self.foundElement is not None:
                self.__changeColorTop()
                self.secondTopClick = self.foundElement
                self.tops[self.firstTopClick].append(self.secondTopClick)
                self.tops[self.secondTopClick].append(self.firstTopClick)
                self.__drawConnectionTops()
                self.secondTopClick = None
                self.firstTopClick = None

        elif self.action == Status.StepPainted:
            self.__findMatch(save_position_x, save_position_y)
            if self.foundElement.index not in self.topsPainted and self.foundElement.index in self.tops2PaintIndex:
                for number, label in enumerate(self.frameStepByStep.winfo_children()):
                    label_text = label.cget('text')
                    if label_text[-1] == str(self.foundElement.index + 1):
                        self.frameStepByStep.winfo_children()[number].config(text=label_text + u'\u2713')
                        self.__saveUserAction(number)
                self.__changeColorTop(TOP_COLOR_PAINT)
                self.topsPainted.append(self.foundElement.index)
                if len(self.topsPainted) == len(self.tops2PaintIndex):
                    messagebox.showinfo("", message="Фигура раскрашена!")

        elif self.action == Status.TrainingRegime or self.action == Status.SolvingRegime:
            self.__findMatch(save_position_x, save_position_y)
            if self.foundElement is None:
                return
            if self.currentIndexColoring is None:
                self.__findCorrectColoring()
            if (
                    self.foundElement.index in self.tops2PaintIndex and self.foundElement.index not in self.topsPainted) or self.action == Status.SolvingRegime:
                self.__saveUserAction()
                self.__changeColorTop(TOP_COLOR_PAINT)
                self.topsPainted.append(self.foundElement.index)
            else:
                if self.boxGameRegime.get() == "Тренажер" and self.foundElement.index not in self.topsPainted:
                    messagebox.showerror("Ошибка", "В данной раскраске вершина не должна быть закрашенной")
                    return
            if self.currentIndexColoring is None:
                for number, coloring in enumerate(self.typeColorings):
                    tops2coloring = [i for i in range(len(coloring)) if coloring[i] == 1]
                    if tops2coloring == self.topsPainted:
                        self.__coloringFinished()
                        return
            if len(self.topsPainted) == len(self.tops2PaintIndex) and len(
                    self.topsPainted) > 0 and self.action != Status.SolvingRegime:
                self.__coloringFinished()

    # Смена действия
    ################################
    def __actionAddTop(self):
        self.__normalizeTops()
        self.__clearFrameStepByStep()
        self.frameFoundPaints.pack_forget()
        self.action = Status.AddTop

    def __actionConnectTops(self):
        self.__normalizeTops()
        self.firstTopClick = None
        self.secondTopClick = None
        self.action = Status.ConnectTops

        self.__clearFrameStepByStep()
        self.frameFoundPaints.pack_forget()

    def __actionGetPaint(self):
        """Раскрашиваем вершины"""
        number_paint = self.boxFoundPaints.current()
        self.__clearFrameStepByStep()
        self.tops2PaintIndex = []
        self.labelsStepByStep = {}
        self.topsPainted = []
        self.frameStepByStep.pack(pady=STANDARD_PADY_FRAMES)
        for number_top, value in enumerate(self.typeColorings[number_paint]):
            if value == 1:
                self.tops2PaintIndex.append(number_top)
                self.__initStep(number_top)
                if self.boxTypeGameRegime.get() != "Раскрашу сам":
                    DrawCircle(self.canvas, list(self.tops.keys())[number_top], number_top, color=TOP_COLOR_PAINT)
                    if self.boxTypeGameRegime.get() == "Анимировано":
                        time.sleep(ANIMATE_PAUSE)
                        self.update()
            else:
                DrawCircle(self.canvas, list(self.tops.keys())[number_top], number_top, color=TOP_COLOR)

        if self.boxTypeGameRegime.get() == "Раскрашу сам":
            self.action = Status.StepPainted
        else:
            self.action = Status.Nothing

    def __revertAction(self):
        """Отменяет последнюю раскраску пользователя"""
        if len(self.userActions) == 0:
            return

        last_action = self.userActions.pop()
        self.topsPainted = last_action['topsPainted']
        DrawCircle(self.canvas, last_action['top'], last_action['top'].index)

        if last_action["numberLabel"] is not None:
            label_text = self.frameStepByStep.winfo_children()[last_action["numberLabel"]].cget('text')
            label_text = label_text[:len(label_text) - 1]
            self.frameStepByStep.winfo_children()[last_action["numberLabel"]].config(text=label_text)

        if last_action["typeColorings"] is not None:
            self.typeColorings = last_action["typeColorings"]
            self.currentIndexColoring = last_action["currentIndexColoring"]

    def __actionClearCanvas(self):
        self.action = Status.Nothing
        self.tops.clear()
        self.numberTop = 0
        self.canvas.delete("all")

        self.__clearFrameStepByStep()
        self.frameFoundPaints.pack_forget()

    ##################################

    def __coloringFinished(self):
        """Уведомляет пользователя, о том что он правильно раскрасил фигуру"""
        messagebox.showinfo("", message="Фигура раскрашена!")
        self.currentIndexColoring = None

    def __findCorrectColoring(self):
        """Используется в режим тренажре или игра.
         Ищет подходящую раскарску под выбор пользователя"""
        index = self.foundElement.index
        copy_type_coloring = list(self.typeColorings)
        for number, coloring in enumerate(self.typeColorings):
            if coloring[index] == 0:
                copy_type_coloring[number] = None

        copy_type_coloring = [coloring for coloring in copy_type_coloring if coloring is not None]
        if len(copy_type_coloring) == 0 and self.action != Status.SolvingRegime:
            return

        if len(self.typeColorings) > 1:
            self.__saveUserAction()
            self.typeColorings = copy_type_coloring
            self.currentIndexColoring = None
            self.tops2PaintIndex = []
            DrawCircle(self.canvas, self.foundElement, self.foundElement.index, TOP_COLOR_PAINT)
            self.topsPainted.append(self.foundElement.index)
        else:
            self.currentIndexColoring = 0
            self.tops2PaintIndex = [i for i in range(len(self.typeColorings[self.currentIndexColoring])) if
                                    self.typeColorings[self.currentIndexColoring][i] == 1]

    def __findColorings(self):
        """Нахождения значения раскрасок"""
        if not self.__checkGameRegime():
            return
        self.typeColorings = process(self.tops)
        self.frameFoundPaints.pack(pady=STANDARD_PADY_FRAMES)
        print(self.typeColorings)
        self.boxFoundPaints['values'] = ["Раскраска №" + str(i) for i in range(len(self.typeColorings))]
        self.boxFoundPaints.current(0)

    def __generateGraph(self):
        """Генерация графа"""
        if not self.__checkGameRegime():
            return
        self.__clearFrameStepByStep()
        self.__actionClearCanvas()
        self.topsPainted = []
        self.userActions = []
        self.tops, self.typeColorings = GenerateGraph()
        print(self.typeColorings)

        for top in self.tops.keys():
            DrawCircle(self.canvas, top, self.numberTop)
            self.numberTop += 1
            if self.tops[top] is not None:
                self.firstTopClick = top
                for second_top in self.tops[top]:
                    self.secondTopClick = second_top
                    self.__drawConnectionTops()

        if self.boxGameRegime.get() == "Тренажер":
            self.action = Status.TrainingRegime
        elif self.boxGameRegime.get() == "Задачи":
            self.action = Status.SolvingRegime
        else:
            self.frameFoundPaints.pack(pady=STANDARD_PADY_FRAMES)
            self.boxFoundPaints['values'] = ["Раскраска №" + str(i) for i in range(len(self.typeColorings))]
            self.boxFoundPaints.current(0)

    def __clearFrameStepByStep(self):
        """Очищает по шаговые подсказки"""
        ClearFrame(self.frameStepByStep)
        self.frameStepByStep.pack_forget()
        self.userActions = []

    def __changeColorTop(self, color=TOP_COLOR):
        """Меняет цвет выбранной вершины"""
        DrawCircle(self.canvas, self.foundElement, self.foundElement.index, color=color)

    def __initStep(self, number_step):
        """Создает шаги к раскраске"""
        text = "Закрасьте вершину №" + str(number_step + 1)
        self.labelsStepByStep[number_step] = Label(self.frameStepByStep, text=text, font=self.fontStep, padx=POPUP_PADY)
        self.labelsStepByStep[number_step].pack()

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

    def __checkSolution(self):
        """Проверяет решение задачи в режим "Задания"""
        if len(self.topsPainted) != len(self.tops2PaintIndex):
            messagebox.showerror("Ошибка", "Закрашенно слишком много или мало вершин")
            return
        for top in self.topsPainted:
            if top not in self.tops2PaintIndex:
                messagebox.showerror("Ошибка", " Вершина номер {} не должна быть закрашенна".format(str(top + 1)))
                return
        self.__coloringFinished()

    def __getSolution(self):
        """Показывает решение по шагам"""
        self.frameStepByStep.pack()

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

    def __saveUserAction(self, number_label=None):
        """Сохраняет все последние действия пользователя в словарь и записывает его"""
        user_action = {"topsPainted": None, "numberLabel": None, "Top": None, "typeColorings": None}
        user_action["topsPainted"] = list(self.topsPainted)
        user_action['top'] = copy.copy(self.foundElement)
        user_action['numberLabel'] = number_label

        if self.boxGameRegime != "Демонстрация":
            user_action["typeColorings"] = self.typeColorings
            user_action["currentIndexColoring"] = self.currentIndexColoring
        self.userActions.append(dict(user_action))

    def __callbackBoxGameRegime(self, event):
        """Коллбек на комбобокс с гейм режимом"""

        value = self.boxGameRegime.get()
        self.boxTypeGameRegime['state'] = 'readonly'
        if value == "Демонстрация":
            self.buttonReverse.pack_forget()
            # иницализация интерфейса демонстрации
            self.boxTypeGameRegime.pack()
            self.boxTypeGameRegime['values'] = DEMONSTRATE_REGIME

        elif value == "Тренажер":
            # инициализация интерфейса тренажера
            self.boxTypeGameRegime.pack_forget()
            self.buttonReverse.pack()
        elif value == "Задачи":
            self.boxTypeGameRegime.pack_forget()
            self.buttonReverse.pack()
            self.frameSolveColorings.pack()
        self.__actionClearCanvas()
        self.boxTypeGameRegime.set('')

    def __callbackBoxTypeGameRegime(self, event):
        """Коллбек на выбор режима игры"""
        self.__normalizeTops()

        if self.boxGameRegime.get() != "Демонстрация":
            self.frameGenerateGraph.pack()
        if self.boxGameRegime.get() == "Демонстрация":
            if self.boxTypeGameRegime.get() == "Раскрашу сам":
                self.buttonReverse.pack()
            else:
                self.buttonReverse.pack_forget()

    def __checkGameRegime(self):
        """Проверяет выбраны ли режимы рисования"""
        if self.boxGameRegime.get() == '' or (
                self.boxGameRegime.get() == "Демонстрация" and self.boxTypeGameRegime.get() == ""):
            messagebox.showerror("Ошибка", "Выберите параметры отображения")
            return False
        return True

    def __callbackBoxFoundPaints(self, event):
        """Коллбек на выбор раскраски"""
        self.__normalizeTops()
        self.__clearFrameStepByStep()

    def __callbackBoxCreateRegime(self, event):
        self.boxGameRegime["state"] = "readonly"
        self.__actionClearCanvas()
        self.__clearFrameStepByStep()
        if self.boxCreateRegime.get() == "Генерация фигуры":
            self.frameCreateBySelf.pack_forget()
            self.frameGenerateGraph.pack()
        elif self.boxCreateRegime.get() == "Построение фигуры":
            self.frameGenerateGraph.pack_forget()
            self.frameCreateBySelf.pack()
        elif self.boxCreateRegime.get() == "Задача Леонардо":
            pass
