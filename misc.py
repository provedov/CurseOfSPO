from Libs import *
def AddButton(txt,func):
    """
        Создание кнопки в интерфейсе.
    Параметры:
        txt - Текст на кнопке.
        func - Функция, которую кнопка запустит после нажатия
    """
    # Создание кнопки
    butt = ttk.Button(text=txt,command=func)
    # Расположение кнопки
    butt.pack(fill=X)
def AddLabel(root,txt,x=0,y=0,IsPack = True,anchor="center"):
    """
        Создание метки в интерфейсе.
    Параметры:
        root - Родительское окно.
        txt - Текст метки.
        x, y - Координаты (если IsPack=False).
        IsPack - Использовать pack() или place().
        anchor - Расположение в окне (если IsPack=True).
    """
    # Создание метки
    label = Label(root, text=txt)
    # Выбор метода расположения
    if (x!=0 and y!=0) or IsPack == False:
        label.place(x=x, y=y)
    else:
        label.pack(anchor = anchor)
def CreateTree(root,dataframe,labelName,x=0,y=0,IsPack = True,width = 150,height = 80,width_h = 100,pady = 0):
    """
        Создание таблицы в интерфейсе.
    Параметры:
        root - Родительское окно.
        dataframe - Таблица базы данных
        labelName - Название таблицы.
        x, y - Координаты (если IsPack=False).
        IsPack - Использовать pack() или place().
        width/height - Ширина/Длинна таблицы
        width_h - Ширина строки
        pady - Длинна отступа
    """
    # Создание метки
    AddLabel(root,labelName,x=(x+width/2)-30,y=y,IsPack = IsPack)
    # Создание таблицы
    tree = ttk.Treeview(root, show="headings")
    # Присваивание название столбикам таблицы
    tree["columns"] = list(dataframe.columns)
    # Заполнение данными
    for column in dataframe.columns:
        tree.heading(column, text=column)
        tree.column(column, width=width_h)
    for index, row in dataframe.iterrows():
        tree.insert("", "end", values=list(row))
    # Выбор метода размещения
    if (x!=0 and y!=0) or IsPack == False:
        tree.place(x=x, y=y+22, width=width, height=height)
    else:
        tree.pack(pady = pady)
def AutomaticSizeWindow(root):
    """
        Автоматизация ширины окна (Работает только с виджитами, которые используют place()!)
    Параметры:
        root - Окно для расширения.
    """
    # Обновляем окно, чтобы все виджеты были отрисованы
    root.update_idletasks()

    # Получаем размеры всех виджетов, размещённых с помощью place
    max_x = 0
    max_y = 0
    for widget in root.winfo_children():
        if isinstance(widget, (Label, ttk.Treeview)):
            widget_x = widget.winfo_x() + widget.winfo_width()
            widget_y = widget.winfo_y() + widget.winfo_height()
            if widget_x > max_x:
                max_x = widget_x
            if widget_y > max_y:
                max_y = widget_y

    # Устанавливаем размеры окна с небольшим отступом
    root.geometry(f"{max_x + 20}x{max_y + 20}")
