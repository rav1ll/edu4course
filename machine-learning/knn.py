import numpy as np
from matplotlib import pyplot as plt
from sklearn import datasets
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score

iris = datasets.load_iris()

# x max и x min
min = iris['data'][0][0]
max = iris['data'][0][0]
for lst in iris['data']:

    for item in lst:
        if item < min:
            min = item
        if item > max:
            max = item

# преобразуем в список
iris_data = []
for lst in iris['data']:

    local_lst = []
    for item in lst:
        local_lst.append(item)
    iris_data.append(local_lst)

# нормализуем данные
iris_norm_data = []
for lst in iris['data']:

    local_lst = []
    for item in lst:
        local_lst.append(round(((item - min) / (max - min)), 4))
    iris_norm_data.append(local_lst)

x = iris_norm_data
y = iris['target']

iris_data = iris_norm_data

# разделяем на тестовые и обучающие выборки
# немного изменено, если делить поровну 5/45 и не перемешивать, К всегда будет равно 1


x_train, x_test, y_train, y_test = train_test_split(iris.data[:, ],
                                                    iris['target'],
                                                    random_state=0,
                                                    test_size=0.6)  # random_state - для воспроизводимости

print(f'X_train shape: {x_train.shape}, y_train shape: {y_train.shape},\n'
      f'X_test shape: {x_test.shape}, y_test shape: {y_test.shape}')

# строим графики
fig, axs = plt.subplots(1, 6, figsize=(30, 5))
fig.suptitle('Проекции на оси до нормализации')
a = 0
for i in range(4):
    for j in range(i + 1, 4):
        axs[a].scatter([elem[i] for elem in iris_data], [elem[j] for elem in iris_data], c=iris['target'])

        axs[a].set_xlabel(iris.feature_names[i])
        axs[a].set_ylabel(iris.feature_names[j])

        a += 1

plt.show()

fig, axs = plt.subplots(1, 6, figsize=(30, 5))
fig.suptitle('Проекции на оси после нормализации')
a = 0
for i in range(4):
    for j in range(i + 1, 4):
        axs[a].scatter([elem[i] for elem in iris_norm_data], [elem[j] for elem in iris_norm_data], c=iris['target'])

        axs[a].set_xlabel(iris.feature_names[i])
        axs[a].set_ylabel(iris.feature_names[j])

        a += 1

plt.show()

# применяем knn


accuracy = 0
k = 0
for i in range(21):
    knn = KNeighborsClassifier(n_neighbors=i + 1)
    knn_model_1 = knn.fit(x_train, y_train)
    knn_predictions_1 = knn_model_1.predict(x_test)
    accuracy_1 = accuracy_score(y_test, knn_predictions_1)
    print('текущая точность для k=', i, accuracy_1)
    if accuracy_1 > accuracy:
        accuracy = accuracy_1
        k = i + 1

print('точность модели:', accuracy, 'k_num:', k)

while True:
    my_list = input("Введите список: ").split()

    for i in range(len(my_list)):
        my_list[i] = float(my_list[i])

    values = my_list[:-1:]

    zz = []
    for item in values:
        zz.append(round(((item - min) / (max - min)), 4))

    target = my_list[-1]
    x_train = np.vstack((x_train, np.array(zz)))
    y_train = np.append(y_train, target)
    accuracy = 0
    knn = KNeighborsClassifier(n_neighbors=k + 1)
    knn_model_1 = knn.fit(x_train, y_train)
    knn_predictions_1 = knn_model_1.predict(x_test)

    accuracy_1 = accuracy_score(y_test, knn_predictions_1)
    if accuracy_1 > accuracy:
        accuracy = accuracy_1
        k = i + 1
    print(f'X_train new shape: {x_train.shape}')
    print('точность модели:', accuracy, 'k_num:', k)
