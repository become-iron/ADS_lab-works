# -*- coding: utf-8 -*-
"""Реализация жадного алгоритма для задачи коммивояжёра"""


inf = float('inf')  # бесконечность


def greedy(matrix):
    """
    Поиск пути жадным алгоритмом
        matrix - матрица расстояний между точками
    """
    path = [0]
    sumOfPath = 0
    for j in range(len(matrix)):  # заполняем пути к стартовому городу inf-ами
        matrix[j][0] = inf
    i = 0
    _ = 1
    while _ != len(matrix):
        minDistance = min(matrix[i])
        indexMinDistance = matrix[i].index(minDistance)
        for j in range(len(matrix)):
            matrix[j][indexMinDistance] = inf
        path += [indexMinDistance]
        sumOfPath += minDistance
        i = indexMinDistance
        _ += 1
    return path, sumOfPath


def plot(coord, path):
    """
    Построение графика по точкам и пути
        coord - координаты точек
        path - путь
    """
    import matplotlib.pyplot as plt
    # генерация имён точек
    # построение графика
    plt.text(coord[0][0], coord[0][1], 'START')
    for i in range(len(coord)):
        plt.scatter(coord[i][0], coord[i][1])
        # plt.text(coord[i][0], coord[i][1] + 1, str(i + 1))
    for i in range(len(path) - 1):
        plt.pause(.5)
        plt.plot([coord[path[i]][0], coord[path[i + 1]][0]], [coord[path[i]][1], coord[path[i + 1]][1]])
    plt.text(coord[path[-1]][0], coord[path[-1]][1], 'FINISH')
    plt.show()
