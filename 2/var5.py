# -*- coding: utf-8 -*-


def is_identity_matrix(matrix):
    is_identity = True
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if (matrix[i][j] != 0 and i != j) or (matrix[i][i] != 1 and i == j):
                is_identity = False
                break
    return is_identity

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
    print(is_identity_matrix(exampleMatrix))

    n = randrange(4, 10)
    print(is_identity_matrix([[0 if i != j else 1 for j in range(n)] for i in range(n)]))

