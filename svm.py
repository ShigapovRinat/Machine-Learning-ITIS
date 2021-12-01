import random
import numpy as np
import pygame
from sklearn.svm import SVC


def generate(point_count, class_count):
    radius = 50
    data = []
    for class_num in range(class_count):
        center_x, center_y = random.randint(radius, width - radius), random.randint(radius, height - radius)
        for row_num in range(point_count):
            data.append([[random.gauss(center_x, radius / 2), random.gauss(center_y, radius / 2)], class_num])
    return data


def get_line_coords(svc):
    w = svc.coef_[0]
    a = -w[0] / w[1]
    xx = np.array([0, width])
    yy = a * xx - (svc.intercept_[0]) / w[1]

    return [xx[0], yy[0]], [xx[-1], yy[-1]]


def draw_pygame():
    screen = pygame.display.set_mode((width, height))
    screen.fill('WHITE')
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = list(event.pos)
                cls = svc.predict([pos])[0]
                points.append([pos, cls])

        for point in points:
            pygame.draw.circle(screen, colors[point[1]], point[0], 3)

        pygame.draw.line(screen, 'red', p1, p2, 1)
        pygame.display.update()


if __name__ == '__main__':
    width, height = 600, 400
    points = generate(5, 2)
    colors = {0: 'green', 1: 'blue'}

    x_list = np.array(list(map(lambda x: x[0], points)))
    y_list = np.array(list(map(lambda x: x[1], points)))

    svc = SVC(kernel='linear')
    svc.fit(x_list, y_list)

    p1, p2 = get_line_coords(svc)

    draw_pygame()
