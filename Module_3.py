from Libs import *
from misc import CreateTree,AutomaticSizeWindow,AddLabel
from Module_2 import Clusterization
def RandomForest(df):
    """
    Классификация кластеров с использованием случайного леса.
    Параметры:
        df (pd.DataFrame): Данные с кластерами из Module_2.
    """
    
    #Кластеризация
    df,tech_data_for_classificators,tech_data = Clusterization(df,False)
    # Признаки
    x = tech_data
    # Целевая переменная
    y = tech_data_for_classificators['Кластер']
    # Разделение данных на обучающую и тестовую выборки
    x_train,x_test, y_train, y_test = train_test_split(x,y,random_state=1,test_size=0.33)
    # Создание модели случайного леса
    RF = RandomForestClassifier(
        n_estimators=500,
        criterion = 'gini',
        bootstrap=True,
        max_features ='sqrt',
        max_depth=10,
        class_weight='balanced',
        min_samples_split=3,
        min_samples_leaf=1,
        oob_score=True)
    # Обучение модели случайного леса
    RF.fit(x_train,y_train)
    res = pd.DataFrame({'Переменная':x.columns,'Значимость':RF.feature_importances_}).sort_values('Значимость')
    y_test_pred = RF.predict(x_test)
    y_train_pred = RF.predict(x_train)
    #Создание окна
    root = Tk()
    root.title("Случайный лес")     
    root.geometry("520x400")
    root.resizable(False, False)
    #Создание таблицы с переменными
    CreateTree(root,res,"Переменные",pady = 10,width_h=250)
    tree = ttk.Treeview(root,show="headings")
    #Создание метки с точностью
    AddLabel(root, txt='Точность: %.3f'% accuracy_score(y_test,y_test_pred),anchor = W)
    r = confusion_matrix(y_train,y_train_pred)
    #Создание метки с матрицей классификации
    AddLabel(root, txt=f'матрица классификации{r}',anchor = W)
    #Создание метки с точностью на обучающей выборке
    acc2 = accuracy_score(y_train,y_train_pred)
    AddLabel(root, txt=f'Точность на обучающей выборке: {acc2}',anchor = W)
    #Визуализация матрицы
    cm1 = confusion_matrix(y_train,y_train_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm1,display_labels=np.unique(y))
    disp.plot(cmap=plt.cm.Greys)
    plt.title('Confusion Matrix')
    plt.show()
    #Сохранение модели
    joblib.dump(RF, 'Output/Models/random_forest_model.pkl')
def NeiroWeb(df):
    """
    Классификация кластеров с использованием нейронной сети.
    Параметры:
        df (pd.DataFrame): Данные с кластерами из Module_2.
    """
    
    df,tech_data_for_classificators,tech_data = Clusterization(df,False)
    x = tech_data
    # Целевая переменная
    y = tech_data_for_classificators['Кластер']
    # Разделение данных на обучающую и тестовую выборки
    x_train,x_test, y_train, y_test = train_test_split(x,y,random_state=1,test_size=0.33)
    
    #Нормирование данных
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    # Преобразуем целевую переменную в one-hot encoding
    num_classes = len(np.unique(y))
    y_train_encoded = to_categorical(y_train -1, num_classes=num_classes)
    y_test_encoded = to_categorical(y_test -1, num_classes=num_classes)

    # Создание модели нейронной сети
    model = Sequential()
    model.add(Dense(128, input_dim=x_train.shape[1], activation='relu'))  # Входной слой
    model.add(Dense(128, activation='relu'))  # Скрытый слой
    model.add(Dense(num_classes, activation='softmax'))  # Выходной слой для многоклассовой классификации

    # Компиляция модели
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
   
    # Обучение модели
    history = model.fit(x_train, y_train_encoded, epochs=50, batch_size=32, validation_split=0.2)

    # Предсказание на тестовых данных
    y_test_pred = model.predict(x_test)
    y_test_pred_classes = np.argmax(y_test_pred, axis=1)+1  # Преобразуем one-hot в классы

    # Предсказание на обучающей выборке
    y_train_pred = model.predict(x_train)
    y_train_pred_classes = np.argmax(y_train_pred, axis=1)+1  # Преобразуем one-hot в классы

    #Создание окна
    root = Tk()
    root.title("Нейросеть")     
    root.geometry("250x50")
    root.resizable(False, False)
    #Создание метки с точностью на тестовой выборке
    AddLabel(root, txt='Точность на тестовой выборке: %.3f' % accuracy_score(y_test, y_test_pred_classes),anchor = W)
    #Создание метки с точностью на обучающей выборке
    AddLabel(root, txt='Точность на обучающей выборке: %.3f' % accuracy_score(y_train, y_train_pred_classes),anchor = W)

    # Матрица для тестовой выборки
    cm_test = confusion_matrix(y_test, y_test_pred_classes)
    disp_test = ConfusionMatrixDisplay(confusion_matrix=cm_test, display_labels=np.unique(y))
    disp_test.plot(cmap=plt.cm.Greys)
    plt.title('Матрица(Test)')
    plt.show()

    # Матрица для обучающей выборки
    cm_train = confusion_matrix(y_train, y_train_pred_classes)
    disp_train = ConfusionMatrixDisplay(confusion_matrix=cm_train, display_labels=np.unique(y))
    disp_train.plot(cmap=plt.cm.Greys)
    plt.title('Матрица(Train)')
    plt.show()

    #Запись модели
    model.save('Output/Models/neural_network_model.h5')
