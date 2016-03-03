# -*- coding: utf-8 -*-
"""
8. Преобразовать матрицу образом, чтобы каждый
столбец был упорядочен по возрастанию
"""


def convert(matrix):
    sortedColons = [sorted([matrix[i][j] for i in range(len(matrix))]) for j in range(len(matrix[0]))]
    return [[sortedColons[j][i] for j in range(len(sortedColons))] for i in range(len(sortedColons[0]))]


if __name__ == '__main__':
    from random import randrange
    from pprint import pprint
    m = randrange(5, 8)  # количество строк
    n = randrange(5, 8)  # количество столбцов
    exampleMatrix = [[randrange(10, 99) for cell in range(n)] for line in range(m)]
    print('Строк: {0}\nСтолбцов: {1}\n'.format(m, n))
    print('Исходная матрица:')
    pprint(exampleMatrix)
    print('\nПреобразованная матрица:')
    pprint(convert(exampleMatrix))
