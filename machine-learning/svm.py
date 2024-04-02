import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.datasets import make_blobs


def add_points(new_points):
    classes = []
    for new_point in new_points:
        predicted_class = clf.predict(new_point)
        classes.append(predicted_class)

        print(predicted_class)
        if predicted_class == 1:
            color = 'red'
        else:
            color = 'blue'
        plt.scatter(new_point[0][0], new_point[0][1], color=color, marker='x')


def graph(X, y, flag=False):
    # Визуализация данных и найденной разделяющей прямой

    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm)

    ax = plt.gca()

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    xx = np.linspace(xlim[0], xlim[1], 30)

    yy = np.linspace(ylim[0], ylim[1], 30)
    YY, XX = np.meshgrid(yy, xx)
    xy = np.vstack([XX.ravel(), YY.ravel()]).T
    Z = clf.decision_function(xy).reshape(XX.shape)
    if flag:
        ax.contour(XX, YY, Z, colors='k', levels=[-1, 0, 1], alpha=0.5, linestyles=['--', '-', '--'])


# Генерация случайной двухклассовой выборки
X, y = make_blobs(n_samples=150, centers=2)

# Обучение модели SVM
clf = svm.SVC(kernel='linear', C=1000)
clf.fit(X, y)

graph(X, y)
# Добавление своей точки
new_points = [[[-4, -2]], [[-4, 5]], [[4, -3]], [[6, 2]], [[4, 5]], [[0, 1]]]
# Предсказание класса для новой точки


add_points(new_points)
graph(X, y, True)

plt.show()
