import numpy as np
from numpy import random
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

node_list = []


n = 50  # Количество вершин в графе
k = 3  # количество кластеров
original_graph = nx.Graph()


# Создание случайной матрицы весов
def generate_weights(n):
    weights = [[0] * n for elem in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            weight = random.randint(1, 30) * random.randint(0, 2)
            weights[i][j] = weight

    return weights


# Вывод графа
def draw_graph(graph):
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.show()


weights = generate_weights(n)

for i in range(n):
    for j in range(i + 1, n):
        if weights[i][j] != 0:
            node_list.append((i, j, weights[i][j]))

print('node list', node_list)

for element in node_list:
    original_graph.add_edge(element[0], element[1], weight=element[2])

draw_graph(original_graph)

sorted_graph = sorted(node_list, key=lambda x: x[2])
united_list = set()  # список соединенных вершин
isolated_nodes = {}  # словарь списка изолированных групп вершин
remain_nodes = []  # список ребер остова
print('sorted', sorted_graph)

for node in sorted_graph:
    if node[0] not in united_list or node[1] not in united_list:  # проверка для исключения циклов в остове
        if node[0] not in united_list and node[1] not in united_list:  # если обе вершины не соединены, то
            isolated_nodes[node[0]] = [node[0], node[1]]  # формируем в словаре ключ с номерами вершин
            isolated_nodes[node[1]] = isolated_nodes[node[0]]  # и связываем их с одним и тем же списком вершин
        else:  # иначе
            if not isolated_nodes.get(node[0]):  # если в словаре нет первой вершины, то
                isolated_nodes[node[1]].append(node[0])  # добавляем в список первую вершину
                isolated_nodes[node[0]] = isolated_nodes[node[1]]  # и добавляем ключ с номером первой вершины
            else:
                isolated_nodes[node[0]].append(node[1])  # иначе, все то же самое делаем со второй вершиной
                isolated_nodes[node[1]] = isolated_nodes[node[0]]

        remain_nodes.append(node)  # добавляем ребро в остов
        united_list.add(node[0])  # добавляем вершины в множество U
        united_list.add(node[1])

for node in sorted_graph:  # проходим по ребрам второй раз и объединяем разрозненные группы вершин
    if node[1] not in isolated_nodes[node[0]]:  # если вершины принадлежат разным группам, то объединяем
        remain_nodes.append(node)  # добавляем ребро в остов
        gr1 = isolated_nodes[node[0]]
        isolated_nodes[node[0]] += isolated_nodes[node[1]]  # объединем списки двух групп вершин
        isolated_nodes[node[1]] += gr1


def dfs(graph, node, cluster):
    cluster.add(node)
    for neighbor in graph.neighbors(node):
        if neighbor not in cluster:
            dfs(graph, neighbor, cluster)


def clusterize_tree(tree):
    clusters = []
    visited = set()
    for node in tree.nodes():
        if node not in visited:
            cluster = set()
            dfs(tree, node, cluster)
            clusters.append(cluster)
            visited.update(cluster)
    return clusters


final_graph = nx.Graph()

for element in remain_nodes:
    final_graph.add_edge(element[0], element[1], weight=element[2])

print(final_graph)

# удаляем все лишние ребра и делаем k кластеров
edges = sorted(final_graph.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
counter = 0

while nx.is_connected(final_graph):
    max_edge = max(final_graph.edges(data=True), key=lambda x: x[2]['weight'])

    # Удалите наибольшее ребро
    final_graph.remove_edge(max_edge[0], max_edge[1])

while counter < k:
    # Найдите наибольшее ребро по весу
    max_edge = max(final_graph.edges(data=True), key=lambda x: x[2]['weight'])

    # Удалите наибольшее ребро
    final_graph.remove_edge(max_edge[0], max_edge[1])

    counter += 1

print(final_graph)

cluster_colors = [0 * i for i in range(n)]

# Разбиение на кластеры
clusters = clusterize_tree(final_graph)
for i, cluster in enumerate(clusters):
    print(f"Кластер {i + 1}: {cluster}")

plt.figure(figsize=(10, 10))
pos = nx.spring_layout(final_graph)
nx.draw(final_graph, pos, with_labels=True)
labels = nx.get_edge_attributes(final_graph, 'weight')
nx.draw_networkx_edge_labels(final_graph, pos, edge_labels=labels)

plt.show()
