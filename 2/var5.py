# -*- coding: utf-8 -*-


def is_identity_matrix(matrix):
    is_identity = True
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if (matrix[i][j] != 0 and i != j) or (matrix[i][i] != 1 and i == j):
                is_identity = False
                break
        if not is_identity:
            break
    return is_identity


if __name__ == '__main__':
    # генерация рандомной неединичной матрицы
    from random import randrange
    from pprint import pprint
    n = randrange(4, 10)  # размер матрицы
    exampleMatrix = [[randrange(10, 99) for cell in range(n)] for line in range(n)]  # генерация матрицы
    print('Неединичная матрица:')
    pprint(exampleMatrix)
    print(is_identity_matrix(exampleMatrix))

    # генерация единичной матрицы
    n = randrange(4, 10)  # размер матрицы
    identity_matrix = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    print('\nЕдиничная матрица:')
    pprint(identity_matrix)
    print(is_identity_matrix(identity_matrix))
