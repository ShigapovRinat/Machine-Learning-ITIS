import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from math import cos, sin, pi


def points_dist(a, b):
    return np.sqrt((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2)


def centroids(points, k):
    x_sum, y_sum = 0, 0
    for i in range(len(points)):
        x_sum += points[i]['x']
        y_sum += points[i]['y']
    x_sum /= len(points)
    y_sum /= len(points)

    center_point = {}
    center_point['x'], center_point['y'] = x_sum, y_sum
    R = 0
    for i in range(len(points)):
        R = max(R, points_dist(center_point, points[i]))
    centroids = []
    for i in range(k):
        centroid = {}
        centroid['x'] = x_sum + R * np.cos(2 * np.pi * i / k)
        centroid['y'] = y_sum + R * np.sin(2 * np.pi * i / k)
        centroids.append(centroid)
    return centroids


def random_points(n):
    points = []
    for i in range(n):
        point = {}
        point['x'] = random.randint(0, 100)
        point['y'] = random.randint(0, 100)
        points.append(point)
    return points


def first_clustering_points(points, centroids):
    cluster_points = [[] for i in range(len(centroids))]
    for i in range(len(points)):
        min = 100
        j_min = 0
        for j in range(len(centroids)):
            dist = points_dist(points[i], centroids[j])
            if dist < min:
                min = dist
                j_min = j
        cluster_points[j_min].append(points[i])
    return cluster_points


def set_matrix(m, points, centroids):
    matrix = [[] for i in range(len(centroids))]
    matrix_false = [[] for i in range(len(centroids))]
    for i in range(len(points)):
        for j in range(len(centroids)):
            for k in range(len(centroids) - 2):
                dist_false = (1 / points_dist(points[i], centroids[j])) ** (1 / (m - 1)) / (
                            1 / points_dist(points[i], centroids[k]) + 1 / points_dist(points[i], centroids[
                        k + 1]) + 1 / points_dist(points[i], centroids[k + 2])) ** (1 / (m - 1))
                dist = (points_dist(points[i], centroids[j])) ** (2 / (1 - m)) / (
                            points_dist(points[i], centroids[k]) + points_dist(points[i],
                                                                               centroids[k + 1]) + points_dist(
                        points[i], centroids[k + 2])) ** (2 / (1 - m))
            matrix_false[j].append(dist_false)
            matrix[j].append(dist)
    return matrix_false


def find_centroids(matrix, k, m, points):
    centroids = []
    for i in range(k):
        x_sum, y_sum, prob = 0, 0, 0
        for j in range(len(points)):
            x_sum += matrix[i][j] ** m * points[i]['x']
            y_sum += matrix[i][j] ** m * points[i]['y']
            prob += matrix[i][j] ** m
        centroid = {}
        centroid['x'] = (x_sum / prob)
        centroid['y'] = (y_sum / prob)
        centroids.append(centroid)
    return centroids


def clustering_points(matrix, points):
    cluster_points = [[] for i in range(len(matrix))]
    for i in range(len(matrix[0])):
        max = 0
        j_max = 0
        for j in range(len(matrix)):
            if matrix[j][i] > max:
                max = matrix[j][i]
                j_max = j
        cluster_points[j_max].append(points[i])
    return cluster_points


def find_max_in_matrixs(matrix1, matrix2):
    res = 0
    for i in range(len(matrix1)):
        for j in range(len(matrix1)):
            res = max(res, abs(matrix2[i][j] - matrix1[i][j]))
    return res

def plotting(centroids, cluster_points):
  color_list = ['g','b','m', 'y', 'c', 'k']

  for k in range(len(centroids)):
    plt.scatter([i['x'] for i in cluster_points[k]], [i['y'] for i in cluster_points[k]], color=color_list[k])
  plt.scatter([i['x'] for i in centroids], [i['y'] for i in centroids], color = 'r')
  plt.draw()
  plt.show()

if __name__ == "__main__":
   n = 100
   k=3
   eps=0.02
   m=2
   points = random_points(n)
   centroids = centroids(points, k)

   cluster_points = first_clustering_points(points, centroids)
   print('centroids', centroids)
   print('cluster_points', cluster_points)

   matrix = set_matrix(m, points, centroids)
   print('sum:', matrix[0][0] + matrix[1][0] + matrix[2][0])
   centroids = find_centroids(matrix, k, m, points)
   print('centroids', centroids)
   new_cluster_points = clustering_points(matrix, points)
   print('new_cluster_points', new_cluster_points)
   plotting(centroids, new_cluster_points)

   matrix_list = []
   matrix_list.append(matrix)

   max_in_matrix = 100.0
   i = 0

   while (max_in_matrix > eps):
       matrix = set_matrix(m, points, centroids)
       centroids = find_centroids(matrix, k, m, points)
       print('centroids =', centroids)
       new_cluster_points = clustering_points(matrix, points)
       print('new_cluster_points', new_cluster_points)
       plotting(centroids, new_cluster_points)
       # print('sum:',(matrix[0][0]+matrix[1][0]+matrix[2][0]))
       matrix_list.append(matrix)

       max_in_matrix = find_max_in_matrixs(matrix_list[i], matrix_list[i + 1])
       i += 1
       print('max_in_matrix =', max_in_matrix)