# -*- coding: utf-8 -*-
"""Реализация алгоритма ближайшего соседа для задачи коммивояжёра"""

inf = float('inf')  # бесконечность


def find_path(matrix):
    """
    ПОИСК ПУТИ
    Принимает:
        matrix - матрица расстояний между точками
    Возвращает:
        path - последовательный список точек для перемещения
        sumOfPath - сумма пути
    """
    path = [0]
    sumOfPath = 0
    for j in range(len(matrix)):  # заполняем пути к стартовому городу inf-ами
        matrix[j][0] = inf
    i = 0
    _ = 1
    while _ != len(matrix):
        minDistance = min(matrix[i])  # ближайшайшай точка
        indexMinDistance = matrix[i].index(minDistance)  # номер ближайшей точки
        for j in range(len(matrix)):  # заполняем пути к ближайшей точке inf-ами
            matrix[j][indexMinDistance] = inf
        path += [indexMinDistance]
        sumOfPath += minDistance
        i = indexMinDistance
        _ += 1
    return path, sumOfPath


def plot(coord, path):
    """
    ПОСТРОЕНИЕ ГРАФИКА ПО ТОЧКАМ И ПУТИ
    Принимает:
        coord - координаты точек
        path - путь
    """
    import matplotlib.pyplot as plt
    plt.text(coord[0][0], coord[0][1], 'START')  # начальная точка
    for i in range(len(coord)):
        plt.scatter(coord[i][0], coord[i][1])  # отмечаем точку
        # plt.text(coord[i][0], coord[i][1] + 1, str(i + 1))
    # вывод пути
    for i in range(len(path) - 1):
        plt.pause(.5)  # пауза между выводами
        plt.plot([coord[path[i]][0], coord[path[i + 1]][0]], [coord[path[i]][1], coord[path[i + 1]][1]])
    plt.text(coord[path[-1]][0], coord[path[-1]][1], 'FINISH')   # конечная точка
    plt.show()
