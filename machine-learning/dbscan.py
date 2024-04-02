import pygame
import matplotlib.pyplot as plt
from math import dist

colors = ["purple", "blue", "orange", "gray", "brown", "aqua", "violet", "gold"]


class Point:
    position: tuple
    flag_color = None
    in_cluster: bool = False

    def __init__(self, position: tuple):
        self.position = position

    def __repr__(self):
        return f"{self.position} {self.flag_color}"


def draw_points(points, screen, radius, color=None):
    for point in points:
        pygame.draw.circle(screen, color if color else point.flag_color, point.position, radius=radius)
    pygame.display.update()


def clear_cluster_flags(cluster, softly: bool = False):
    for point in cluster:
        point.in_cluster = False
        if softly and point.flag_color == "black":
            continue
        point.flag_color = None


def set_color_to_neighbours(neighbours_cluster, points, neighbours_count, i):
    if len(neighbours_cluster) < neighbours_count:
        points[i].flag_color = "black"
        for point in neighbours_cluster:
            point.flag_color = "black"
            point.in_cluster = False
    else:
        points[i].flag_color = "green"
        points[i].in_cluster = True
        for point in neighbours_cluster:
            if point.flag_color == "black":
                point.flag_color = "yellow"
            else:
                point.flag_color = "green"


def find_neighbours(point, points, r):
    neighbours = []
    for i in range(len(points)):
        if dist(points[i].position, point.position) <= r and points[i] != point and not points[i].in_cluster:
            neighbours.append(points[i])
            points[i].in_cluster = True
    return neighbours


def deep_find_neighbours(start_neighbours: list, points, r):
    stack = [x for x in start_neighbours]
    while len(stack) != 0:
        point = stack.pop()
        neighbours = find_neighbours(point, points, r)
        for neighbour in neighbours:
            start_neighbours.append(neighbour)
            stack.append(neighbour)
    return start_neighbours


def arrange_points(points, screen, radius):
    clear_cluster_flags(points, softly=True)
    clusters = []
    neighbours_count = 4
    r = 60
    for i in range(len(points)):
        if points[i].in_cluster:
            continue
        neighbours = deep_find_neighbours(find_neighbours(points[i], points, r), points, r)
        set_color_to_neighbours(neighbours, points, neighbours_count, i)
        if len(neighbours) > neighbours_count:
            clusters.append(neighbours)
    draw_points(points, screen, radius)
    return clusters


def draw_clusters(clusters, screen, radius):
    for color_index, cluster in enumerate(clusters):
        draw_points(cluster, screen, radius, color=colors[color_index])
        clear_cluster_flags(cluster)


def main():
    radius = 5
    height = 800
    width = 1200
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    flag = True
    mouse_button_down = False

    points = []
    clusters = []

    screen.fill("white")

    pygame.display.update()

    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    clusters = arrange_points(points, screen, radius)

                    for point in points:
                        plt.scatter(point.position[0], height - point.position[1], color=point.flag_color)
                    plt.show()


                elif event.key == pygame.K_SPACE:
                    draw_clusters(clusters, screen, radius)

                    for poin in points:
                        plt.scatter(poin.position[0], height - poin.position[1], color='black')
                    for cluster_num in range(len(clusters)):

                        for point in clusters[cluster_num]:
                            plt.scatter(point.position[0], height - point.position[1], color=colors[cluster_num])
                    plt.show()


            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_button_down = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_button_down = False

            if mouse_button_down and event.dict.get("pos"):
                pos = event.pos
                if len(points):
                    if dist(pos, points[-1].position) > 10 * radius:
                        pygame.draw.circle(screen, "red", pos, radius=radius)
                        points.append(Point(pos))
                else:
                    pygame.draw.circle(screen, "red", pos, radius=radius)
                    points.append(Point(pos))

            pygame.display.update()
    return points


if __name__ == '__main__':
    main()
