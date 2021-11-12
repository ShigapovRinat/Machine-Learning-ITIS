import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def dist(a, b):
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
        R = max(R, dist(center_point, points[i]))
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


def kmeansWithDraw(points, centroids):
    diff = 1
    cluster = np.zeros(len(points))
    while diff:
        for i, point in enumerate(points):
            mn_dist = float('inf')
            for j, centroid in enumerate(centroids):
                d = dist(centroid, point);
                if mn_dist > d:
                    mn_dist = d
                    cluster[i] = j
        new_centroids = pd.DataFrame(points).groupby(by=cluster).mean().to_dict('records')

        for i, p in enumerate(points):
            plt.scatter(p['x'], p['y'], color=colors[int(cluster[i])])
        plt.scatter([p['x'] for p in new_centroids], [p['y'] for p in new_centroids], color='r')
        plt.show()

        if centroids == new_centroids:
            diff = 0
        else:
            centroids = new_centroids
    return centroids, cluster


def kmeans(points, centroids):
    diff = 1
    cluster = np.zeros(len(points))
    while diff:
        for i, point in enumerate(points):
            mn_dist = float('inf')
            for j, centroid in enumerate(centroids):
                d = dist(centroid, point);
                if mn_dist > d:
                    mn_dist = d
                    cluster[i] = j
        new_centroids = pd.DataFrame(points).groupby(by=cluster).mean().to_dict('records')

        if centroids == new_centroids:
            diff = 0
        else:
            centroids = new_centroids
    return centroids, cluster


def calculate_cost(points, centroids, cluster):
    sum = 0
    for i, point in enumerate(points):
        sum += dist(point, centroids[int(cluster[i])])
    return sum


if __name__ == "__main__":
    n = 100
    points = random_points(n)

    # plt.scatter([p['x'] for p in points], [p['y'] for p in points])
    # centroids = centroids(points, k)
    # plt.scatter([p['x'] for p in centroids], [p['y'] for p in centroids], color = 'r')
    # plt.show()

    cost_list = []
    for k in range(1, 10):
        centroids_list = centroids(points, k)
        centroids_list, cluster = kmeans(points, centroids_list)
        cost = calculate_cost(points, centroids_list, cluster)
        cost_list.append(cost)

    sns.lineplot(x=range(1, 10), y=cost_list, marker='o')
    plt.xlabel('k')
    plt.ylabel('sum')
    plt.show()

    k_min = 1;
    val_min = float('inf')
    for i in range(1, 8):
        val = abs(cost_list[i + 1] - cost_list[i]) / abs(cost_list[i - 1] - cost_list[i])
        if (val < val_min):
            k_min = i
            val_min = val
            print(k_min)
            print(val_min)

    print(k_min)
    centroids_list = centroids(points, k_min)
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    centroids_list, cluster = kmeansWithDraw(points, centroids_list);

    for i, p in enumerate(points):
        plt.scatter(p['x'], p['y'], color=colors[int(cluster[i])])
    plt.scatter([p['x'] for p in centroids_list], [p['y'] for p in centroids_list], color='r')
    plt.show()
