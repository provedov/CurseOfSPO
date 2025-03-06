from Libs import *
from misc import CreateTree,AutomaticSizeWindow,AddLabel

def Kvartill(name,df):
    
    """
    Анализ распределения данных по квартилям для указанного признака.
    Параметры:
        name - Название столбца для анализа.
        df - начальная таблица базы данных.
    """
    
    # Квартили
    q1 = df[name].describe().loc["25%"]
    q2 = df[name].describe().loc["50%"]
    q3 = df[name].describe().loc["75%"]
    # Распределение квартилей    
    kvartill_1 = df[df[name] < q1].groupby('Регион')[name].max().reset_index();
    kvartill_2 = df[(df[name] > q1) & (df[name] < q2)].groupby('Регион')[name].max().reset_index();
    kvartill_3 = df[(df[name] > q2) & (df[name] < q3)].groupby('Регион')[name].max().reset_index();
    kvartill_4 = df[df[name] > q3].groupby('Регион')[name].max().reset_index();

    # Создание окна
    root = Tk()
    root.title("Квартили по " + name)     
    root.resizable(False, False)
    # Создание колонок
    CreateTree(root,kvartill_1,"1 Квартиль",x=10,y=10,width = 300,height = 300)
    CreateTree(root,kvartill_2,"2 Квартиль",x=320,y=10,width = 300,height = 300)
    CreateTree(root,kvartill_3,"3 Квартиль",x=630,y=10,width = 300,height = 300)
    CreateTree(root,kvartill_4,"4 Квартиль",x=940,y=10,width = 300,height = 300)
    # Создание меток для квартилей
    AddLabel(root,f"25% квартиль: {q1}",x = 10,y=340)
    AddLabel(root,f"50% квартиль: {q2}",x=10, y=360)
    AddLabel(root,f"75% квартиль: {q3}",x=10, y=380)
    # Автоматическое разширенние окна
    AutomaticSizeWindow(root)
    
    root.mainloop()
def PrintPValue(p_value,root):
    """
    Вывод результата анализа в виде текстовой метки в интерфейсе.
    Параметры:
        p_value - Рассчитанное p-значение.
        root - Окно для вывода результата.
    """
    alpha = 0.05 # Уровень значимости
    if (p_value < alpha).any():
        AddLabel(root,"Отвергаем нулевую гипотезу: средние значения статистически значимо отличаются.",anchor=W)
    else:
        AddLabel(root,"Не отвергаем нулевую гипотезу: средние значения не отличаются статистически значимо.",anchor=W)
    
def TestT(root,control_group, test_group):
    
    """
    Тестирование при помощи t-критерия
    Параметры:
        root - Окно для вывода результата.
        control_group - Контрольная группа
        test_group - Тестовая группа
    """
    
    #Добавление метки t-критерии
    AddLabel(root,'t-критерии')
    #t - тестированиие
    t_stat, p_value = ttest_ind(control_group, test_group)
    #Вывод в интерфейс T-статистики и P-значения
    AddLabel(root,f'T-статистика: {t_stat}',anchor=W)
    AddLabel(root,f'P-значение: {p_value}',anchor=W)
    #Вывод результата анализа в виде текстовой метки в интерфейсе.
    PrintPValue(p_value,root)
def MannWhitneyCriterua(root,control_group, test_group):

    """
    Тестирование при помощи критерия Манна-Уитнии
    Параметры:
        root - Окно для вывода результата.
        control_group - Контрольная группа
        test_group - Тестовая группа
    """
    #Добавление метки t-критерии
    AddLabel(root,'Критерий Манна-Уитни')
    
    #Тестирование критерием
    t_stat, p_value = mannwhitneyu(control_group, test_group, alternative='two-sided')

    #Вывод в интерфейс T-статистики и P-значения
    AddLabel(root,f'U-статистика: {t_stat}',anchor=W)
    AddLabel(root,f'P-значение: {p_value}',anchor=W)
    #Вывод результата анализа в виде текстовой метки в интерфейсе.
    PrintPValue(p_value,root)
def AnalyzeInformationCRMAndSCMSystem(df):

    """
    Анализ Информации по CRM-системам и SCM-системам.
    Функция выводит окно с результатами T-тестирования и тестирования критерием Маннна-Уитнии, а так же выводит таблицу со средними значениями CRM-систем и SCM-систем по федеральным округам
    Параметры:
        df(dataFrame) - начальная таблица базы данных
    """
    # Группировка по федеральным округам и вычисление среднего
    CRM_systems = df.groupby('Федеральный_округ')['CRM-системы'].mean().reset_index()
    SCM_systems = df.groupby('Федеральный_округ')['SCM-системы'].mean().reset_index()

    # Объединение данных
    result = pd.concat([CRM_systems, SCM_systems['SCM-системы']], axis=1)
    
    # Подготовка к тестированию
    result = result.rename(columns = {'Федеральный_округ':'Федеральный округ'})
    result_research = result.drop(columns = 'Федеральный округ')
    control_group, test_group = train_test_split(result_research, test_size=0.5, random_state=42)

    #Создание окна
    root = Tk()
    root.title("Анализ по CRM и SCM системам")     
    root.resizable(False, False)

    #Тестирование T-критерием
    TestT(root,control_group, test_group)

    #Создание разделительной черты
    separator = ttk.Separator(root, orient="horizontal")
    separator.pack(fill="x", pady=10)

    # Тестирование критерием Манна-Уитни
    MannWhitneyCriterua(root,control_group, test_group)
    
    # Сохранение результата
    result.to_excel('Output/Результат.xlsx', index=False)
def PrintFirstAndEndDataFrame(df):
    """
    Отображает первые 10 и последние 10 строк таблицы
    Параметры:
        df(dataFrame) - начальная таблица базы данных
        name - название столбца
        color_g - Цвет гистограммы
    """
    # Создание окна
    root = Tk()
    root.title("Первые 10 и первые 10 последних записи")     
    root.geometry("1500x550")
    root.resizable(False, False)

    # Выделение первых 10 и последние 10 строк
    df_head = df.head(10)
    df_tail = df.tail(10)

    # Создание колонок
    CreateTree(root,df_head,"10 Первых",width_h = 50,pady = 10)
    CreateTree(root,df_tail,"10 Последних",width_h = 50,pady = 10)
def BoxPlotAndGippogram(df,name,color_g = 'blue'):
    """
    Создание boxplot и гистограммы для определенного столбца
    Параметры:
        df(dataFrame) - начальная таблица базы данных
        name - название столбца
        color_g - Цвет гистограммы
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    cleanName = name.replace("_", " ")
    # Boxplot
    axes[0].boxplot(df[name])
    axes[0].set_title(f'Boxplot: {cleanName}')
    axes[0].set_ylabel('Значение')

    # Гистограмма
    n = len(df[name])
    bins_sturges = int(1 + np.log2(n))

    sns.histplot(df[name], bins=bins_sturges, kde=True, color = color_g, alpha=0.7, ax=axes[1])
    axes[1].set_title(f'Гистограмма {cleanName}')
    axes[1].set_xlabel('Значение')
    axes[1].set_ylabel('Частота')
    axes[1].grid(axis='y', alpha=0.75)

    # Настройка общего заголовка
    plt.suptitle('Анализ данных', fontsize=16)

    # Автоматическая настройка отступов
    plt.tight_layout()

    # Отображение всех графиков
    plt.show()
