import pygame
import random
import numpy as np


def draw_near(x, y):
    points.append((x, y))
    flags.append('red')
    colors.append('red')
    k = random.randint(1, 4)
    d = list(range(-5*r, -2*r)) + list(range(2*r, 5*r))
    for i in range(k):
        x_new = x + random.choice(d)
        y_new = y + random.choice(d)
        points.append((x_new, y_new))
        flags.append('red')
        colors.append('red')


def draw_pygame():
    screen = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
    #окрашиваем
    screen.fill('WHITE')
    play = True
    #чтоб окно быстро не закрывалось и закрывалось на крестик
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    draw_near(event.pos[0], event.pos[1])

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    green_and_yellow()
                    add_colour_point()

            screen.fill('WHITE')
            for i in range(len(points)):
    #при нажатии на кнопку мыши, рисуем круг на нашем скрине, красного цвета, координаты, event.pos - на месте нажатия, радиус 5
                pygame.draw.circle(screen, colors[i], ((points[i][0], points[i][1])), r)

        pygame.display.update()

def dist(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def green_and_yellow():
    #flag = np.zeros(len(points))
    #0 - красный, 1 - желтый, 2 - зеленый
    for i in range(len(points)):
        neighb = 0
        for j in range(len(points)):
            if dist(points[i], points[j]) <= eps and i != j:
                neighb +=1
        if neighb >= minPts:
            flags[i] = 'green'
    for i in range(len(points)):
        if flags[i] != 'green':
            for j in range(len(points)):
                if flags[j] == 'green':
                    if dist(points[i], points[j]) <= eps and i != j:
                        flags[i] = 'yellow'
    for i in range(len(points)):
        if flags[i] == 0:
            flags[i] = 'red'
    #return flag


def add_colour_point():
    color_number = 0
    for i in range(len(points)):
        colors[i] = 'red'
    for i in range(len(points)):
        if colors[i] == 'red' and flags[i] == 'green':
            colors[i] = color_list[color_number]
            for j in range(len(points)):
                if colors[j] == 'red' and (dist(points[i], points[j]) <= eps):
                    colors[j] = color_list[color_number]
            color_number += 1


if __name__ == '__main__':
    r = 4
    points = []
    flags = []
    colors = []
    minPts, eps = 7, 50
    color_list = ['yellow', 'bisque', 'aliceblue', 'blue', 'gray', 'purple', 'mintcream', 'MidnightBlue', 'Goldenrod', 'Brown', 'Black']
    draw_pygame()
    # print(pygame.color.THECOLORS)