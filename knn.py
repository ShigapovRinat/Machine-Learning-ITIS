import random

import numpy as np
import pygame


def dist(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def generate_data(point_count_in_class, number_of_classes):
    radius = 50
    data = []
    for classNum in range(number_of_classes):
        center_x, center_y = random.randint(radius, 600 - radius), random.randint(radius, 400 - radius)
        for rowNum in range(point_count_in_class):
            data.append([[random.gauss(center_x, radius / 2), random.gauss(center_y, radius / 2)], classNum])
    return data


def KNN(point, k):
    sorted_points = sorted_points_by_distance(point)
    nearest_k_points = sorted_points[:k]
    color = get_color(nearest_k_points)
    print("для точки выбран кластер {}".format(colors[color]))
    point[1] = color


def get_color(points):
    color_counts = {}
    for p in points:
        color_counts.setdefault(p[1], 0)
        color_counts[p[1]] += 1

    most_frequent_color_index = 0
    most_frequent_color_count = 0
    for color, color_count in color_counts.items():
        if color_count > most_frequent_color_count:
            most_frequent_color_count = color_count
            most_frequent_color_index = color

    return most_frequent_color_index


def sorted_points_by_distance(point):
    distances = []
    for p in points:
        if point == p:
            continue
        distances.append(dist(p[0], point[0]))

    return [points[x] for x in np.argsort(distances)]


def count_res_k(point):
    sorted_points = sorted_points_by_distance(point)
    for k in range(1, len(k_results)):
        nearest_k_points = sorted_points[:k]
        result_for_current_k = get_color(nearest_k_points)
        if point[1] == result_for_current_k:
            print("при k={} цвет точки определен правильно".format(k))
            k_results[k] += 1
    print("---")


def get_best_k():
    max_result = 0
    max_result_index = -1

    for k_index, k in enumerate(k_results):
        if k > max_result:
            max_result = k
            max_result_index = k_index

    print("k={}, определено {} раз правильно"
          .format(max_result_index, max_result))

    return max_result_index


def draw_pygame():
    global test_index
    screen = pygame.display.set_mode((600, 400))

    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    test_points.append([[event.pos[0], event.pos[1]], -1])

                if event.button == 3:
                    point = [[event.pos[0], event.pos[1]], -1]
                    KNN(point, get_best_k())
                    points.append(point)

            if event.type == pygame.KEYDOWN:

                if len(test_points) > test_index:
                    test_point = test_points[test_index]
                    if event.key == pygame.K_1:
                        test_point[-1] = 0

                    if event.key == pygame.K_2:
                        test_point[-1] = 1

                    if event.key == pygame.K_3:
                        test_point[-1] = 2

                    test_index += 1
                    points.append(test_point)
                    count_res_k(test_point)

        for point in points:
            pygame.draw.circle(screen, colors[point[1]], point[0], 3)
        for point in test_points:
            pygame.draw.circle(screen, colors[point[1]], point[0], 3)

        pygame.display.update()


if __name__ == '__main__':
    n, cl = 20, 3
    colors = ['red', 'green', 'blue', 'white']
    points = generate_data(n, cl)

    test_points = []
    test_index = 0

    print("""точка без кластера - левая кнопка
             добавить в кластер - 1-красный, 2-зеленый, 3-синий
             точка в кластере - правая кнопка
             k будет рассматриваться в промежутке [{}, {}]"""
          .format(0, len(points) - 1))

    k_results = [0 for x in range(int(len(points)))]
    draw_pygame()
