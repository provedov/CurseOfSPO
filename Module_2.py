from Libs import *
from misc import CreateTree,AutomaticSizeWindow,AddLabel

def shift_values(column):
    """
    Удаление NaN-значений из столбца и преобразование в список.
    Параметры:
        column - Исходный столбец с NaN.
    Возвращает:
        pd.Series - Очищенный столбец без NaN.
    """
     # Убираем NaN и преобразуем в список
    non_nan_values = column.dropna().tolist() 
    return pd.Series(non_nan_values)
#Кластеризация
def Clusterization(df,NeedVisual = True):
    """
        Кластеризация
    Параметры:
        df - начальная таблица базы данных.
        NeedVisual - переменная для определения необходимости визуализировать результаты кластеризации.
     Возвращает:
        df - df с добавленным столбцом 'Кластер'.
        tech_data_for_classificators - Данные для классификации.
        tech_data - Стандартизированные данные.
    """
    # Столбцы для кластеризации
    tech_columns = [
    'Персональные_компьютеры', 'Серверы', 'Локальные_сети', 'Облачные_сервисы',
    'Технологии_сбора_больших_данных', 'Интернет_вещей', 'Технологии_искусственного_интелекта',
    'Цифровые_платформы', 'Мобильный_интернет', 'Фиксированный_интернет',
    'Использование_доступа_к_интернету', 'Организации_имеющие_сайт',
    'Использование_специальных_программных_средств', 'Для_научных_исследований', 'Для_проектирования',
    'Для_управления_производством', 'для осуществления финансовых расчетов', 'для предоставления доступа к БД',
    'редакционно-издательские системы', 'Обучающие_системы', 'CRM-системы', 'ERP-системы', 'SCM-системы',
    'Справочно-правовые_системы', 'Прочие_программные_средства'
    ]
    # Заполнение переменной tech_data
    tech_data = df[tech_columns]

    # Копирование данных для класстеров
    tech_data_for_classificators =tech_data.copy()
    # Стандартизация данных 
    tech_data = zscore(tech_data)

    # Иерархическая кластеризация
    Z = linkage(tech_data, method='ward')

    #Разделение на кластеры (например, на 4 кластера)
    clusters = fcluster(Z, t=4, criterion='maxclust')
    df['Кластер'] = clusters
    tech_data_for_classificators['Кластер'] = clusters
    # Если NeedVisual равен False, функция возращает переменные, иначе запускает функцию визуализации
    if NeedVisual == False:
        return df,tech_data_for_classificators,tech_data
    else:
        Visualization(df,Z,tech_columns)
def Visualization(df,Z,tech_columns):
    """
        Визуализация
    Параметры:
        df - начальная таблица базы данных.
        Z - Иерархия кластеризации
        tech_columns - Стандартизированные данные
    """
    # Визуализация дендрограммы
    plt.figure(figsize=(12, 8))
    dendrogram(Z, labels=df['Регион'].values, orientation='top')
    plt.title('Дендрограмма иерархической кластеризации регионов')
    plt.xlabel('Расстояние')
    plt.ylabel('Регионы')
    plt.show()

    # Вывод результатов
    #Разделение кластеров на таблицы
    cluster_1 = ((df[df['Кластер'] == 1].groupby('Регион')['Кластер'].max().reset_index()).drop(columns ='Кластер')).rename(columns={'Регион':'Кластер 1'})
    cluster_2 = ((df[df['Кластер'] == 2].groupby('Регион')['Кластер'].max().reset_index()).drop(columns ='Кластер')).rename(columns={'Регион':'Кластер 2'})
    cluster_3 = ((df[df['Кластер'] == 3].groupby('Регион')['Кластер'].max().reset_index()).drop(columns ='Кластер')).rename(columns={'Регион':'Кластер 3'})
    cluster_4 = ((df[df['Кластер'] == 4].groupby('Регион')['Кластер'].max().reset_index()).drop(columns ='Кластер')).rename(columns={'Регион':'Кластер 4'})
    #Объединение таблиц в одну
    result_cluster = pd.concat([cluster_1 , cluster_2,cluster_3,cluster_4], ignore_index=True)
    #Очистка от NaN
    result_cluster = result_cluster.apply(shift_values, axis=0)
    result_cluster = result_cluster.fillna('')

    #Создание окна
    root = Tk()
    root.title("Кластеризация")     
    root.resizable(True, True)
    #Создание таблицы кластеров в окне
    CreateTree(root,result_cluster,"Кластеры",width_h = 200,pady = 10)
    
    #Создание таблицы средних значении
    mean_values = df[tech_columns].mean()
    result_df = pd.DataFrame({'Название': tech_columns,'Среднее значение': mean_values})
    result_df = result_df.replace('_', ' ', regex=True)
    CreateTree(root,result_df,"Средние значения",width_h = 250,pady = 10)
    
    # Обновление геометрии окна
    root.update_idletasks()

    # Получение размеров содержимого
    width = root.winfo_width()
    height = root.winfo_height()

     # Создание графика средних значений
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Среднее значение', y='Название', data=result_df, ax=ax, palette='viridis')
    ax.set_title('Средние значения по технологиям')
    ax.set_xlabel('Среднее значение')
    ax.set_ylabel('Технологии')

    # Встраивание графика в Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    plt.close()
    root.mainloop()
