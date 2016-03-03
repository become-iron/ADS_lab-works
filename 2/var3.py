# -*- coding: utf-8 -*-
"""
3. Преобразовать матрицу A(m,n) так, чтобы строки с нечетными индексами
были упорядочены по убыванию, c четными - по возрастанию
"""


def convert_matrix(matrix):
    return [sorted(matrix[i]) if i % 2 == 0 else sorted(matrix[i], reverse=True) for i in range(len(matrix))]


if __name__ == '__main__':
    from random import randrange
    from pprint import pprint
    m = randrange(4, 10)  # количество строк
    n = randrange(4, 10)  # количество столбцов
    exampleMatrix = [[randrange(10, 99) for cell in range(n)] for line in range(m)]  # генерация матрицы
    print('Строк: {0}\nСтолбцов: {1}\n'.format(m, n))
    print('Исходная матрица:')
    pprint(exampleMatrix)
    print('\nПреобразованная матрица:')
    pprint(convert_matrix(exampleMatrix))
