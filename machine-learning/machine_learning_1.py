import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

from statistics import mean
from statistics import StatisticsError
from random import randint
from math import dist


def get_center_of_cluster(points: list):
    try:
        return round(mean(list(map(lambda x: x[0], points))), 1), round(mean(list(map(lambda x: x[1], points))), 1)
    except StatisticsError:
        return []


def calculate_shop_points(points, n) -> list:
    x_center, y_center = get_center_of_cluster(points)
    radius = dist((x_center, y_center), points[0])
    for i in range(len(points)):
        if dist((x_center, y_center), points[i]) > radius:
            radius = dist((x_center, y_center), points[i])
    shop_points = [(
        radius * np.cos(2 * np.pi * i / n) + x_center,
        radius * np.sin(2 * np.pi * i / n) + y_center
    ) for i in range(1, n + 1)]

    return shop_points


def set_points_to_clusters(shop_points: list, points: list):
    clusters = [[] for _ in range(len(shop_points))]
    for point in points:
        closest = dist(shop_points[0], point)
        shop_index = 0
        for i in range(1, len(shop_points)):
            if (temp := dist(shop_points[i], point)) < closest:
                closest = temp
                shop_index = i
        clusters[shop_index].append(point)
    return clusters


def show_clustered_points_and_shops(point, shops):
    # show colored
    n = len(shops)
    colors = cm.rainbow(np.linspace(0, 1, n))
    for i, color in zip(range(n), colors):
        plt.scatter(list(map(lambda x: x[0], point[i])), list(map(lambda x: x[1], point[i])), color=color)

    for _ in range(n):
        plt.scatter(list(map(lambda x: x[0], shops)), list(map(lambda x: x[1], shops)),
                    color="black")
    plt.show()


def generate_clusters_and_shops(points, n):
    shop_points = calculate_shop_points(points, n)
    clusters = set_points_to_clusters(shop_points, points)

    # show_clustered_points_and_shops(clusters, shop_points)
    i = 1
    while new_shop_points := [get_center_of_cluster(x) for x in clusters if x != []]:
        if shop_points == new_shop_points:
            break
        shop_points = new_shop_points

        i += 1
        if i % 5000 == 0:
            print(shop_points)
            # show_clustered_points_and_shops(clusters, shop_points)
        clusters = set_points_to_clusters(shop_points, points)
    print("Iterations count: ", i)
    show_clustered_points_and_shops(clusters, shop_points)
    return clusters, shop_points


def calculate_distance_squares(clusters, shops):
    all_clusters_sum = 0
    for i in range(len(shops)):
        temp_sum = 0
        for point in clusters[i]:
            temp_sum += (dist(point, shops[i]) ** 2)
        all_clusters_sum += temp_sum
    return all_clusters_sum


def main():
    points = [(randint(0, 100), randint(1, 100)) for _ in range(100)]  # x y
    iterations = [0] * 10
    for i in range(1, len(iterations)):
        clusters, shops = generate_clusters_and_shops(points, i)
        clusters_sums = calculate_distance_squares(clusters, shops)
        iterations[i] = clusters_sums
    plt.plot([x for x in range(1, len(iterations))], iterations[1:])
    plt.show()
    changes = [abs(iterations[i] - iterations[i + 1]) / abs(iterations[i] - iterations[i - 1]) for i in range(0, len(iterations) - 1)]
    print(changes)
    print(min(changes))

if __name__ == '__main__':
    main()
