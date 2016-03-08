# -*- coding: utf-8 -*-

import nearest_neighbour as nn
from random import randrange
from pprint import pprint
from math import fabs, sqrt
from copy import deepcopy

amountPoints = randrange(5, 10)  # количество точек
coordinates = [[randrange(10, 99), randrange(10, 99)] for i in range(amountPoints)]  # координаты точек

# матрица расстояний между точками
# TODO оптимизировать
distance = [[round(sqrt((fabs(point[0] - _[0])) ** 2 + (fabs(point[1] - _[1])) ** 2), 1) for _ in coordinates] for point in coordinates]

# замена нулей на inf
# TODO возможна ситуация, когда города расположены в одной точке
distance = [[distance[i][j] if distance[i][j] != 0 else nn.inf for i in range(len(distance))] for j in range(len(distance[0]))]

path, sumOfPath = nn.find_path(deepcopy(distance))  # поиск пути

print('Количество точек:\n%s\n' % amountPoints)
print('Координаты точек:')
pprint(coordinates)
print('\nМатрица расстояний между точками:')
pprint(distance)
print('\nПуть:')
print(path)
print('\nСумма пути: %s' % sumOfPath)

nn.plot(coordinates, path)  # визуализация пути
