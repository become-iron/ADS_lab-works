# -*- coding: utf-8 -*-

import greed_algorithm as greed
from random import randrange
from pprint import pprint
from math import fabs, sqrt

amountPoints = randrange(10, 30)  # количество точек
print('Количество точек:\n%s\n' % amountPoints)
# координаты точек
coordinates = [[randrange(10, 99), randrange(10, 99)] for i in range(amountPoints)]
print('Координаты точек:')
pprint(coordinates)
# матрица расстояний между точками
# TODO оптимизировать
distance = [[round(sqrt((fabs(point[0] - _[0])) ** 2 + (fabs(point[1] - _[1])) ** 2), 1) for _ in coordinates] for point in coordinates]
# замена нулей на inf
distance = [[distance[i][j] if distance[i][j] != 0 else greed.inf for i in range(len(distance))] for j in range(len(distance[0]))]
print('\nМатрица расстояний между точками:')
# pprint(distance)

path, sumOfPath = greed.greedy(distance)
print('\nПуть:')
print(path)
print('\nСумма пути: %s' % sumOfPath)

greed.plot(coordinates, path)
