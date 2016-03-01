# -*- coding: utf-8 -*-
"""
Вычислить выражение: [см. приложенное изображение]
"""

from math import factorial, fabs  # высчитывание факториала, модуля числа
from decimal import Decimal  # для точных расчётов

sumOfSeries = 1  # сумма ряда, включая первый его член равный 1


def _val_of_term(n, x):
    """
    Вычисление n-го члена ряда
        n - номер члена ряда
        x - значение величины x
    """
    return Decimal(((-1) ** n) * (x ** (2 * n)) / factorial(2 * n))


def sum_by_accuracy(x):
    """
    Вычисление суммы ряда с заданной точностью
        x - значение величины x
    """
    global sumOfSeries
    precision = int(input('С какой точностью посчитать ряд (знаков после запятой)? (от 1 до 28)\n'))

    i = 0
    while True:
        i += 1
        valueOfTerm = _val_of_term(i, x)  # значение n-го члена ряда
        if fabs(valueOfTerm) < 10 ** (-precision):  # е. значение n-го члена ряда меньше требуемой точности
            break
        sumOfSeries = Decimal(sumOfSeries + valueOfTerm)
    return sumOfSeries


def sum_by_amount_of_terms(x):
    """
    Вычисление суммы ряда с заданным количеством членов ряда
        x - значение величины x
    """
    global sumOfSeries
    amountOfTerms = int(input('Введите количество членов ряда для вычисления его суммы (>=1)\n'))  # количество членов ряда
    for i in range(amountOfTerms - 1):  # вычитание - для первого члена ряда
        sumOfSeries = Decimal(sumOfSeries + _val_of_term(i, x))
    return sumOfSeries


if __name__ == '__main__':
    x = int(input('Задайте величину x\n'))
    while True:
        command = input('''Выберите метод подсчёта суммы ряда, введя соответствующую команду:\n[0] - по заданной точности\n[1] - с заданным количеством членов ряда\n''')
        if command == '0':
            sumOfSeries = sum_by_accuracy(x)
            break
        elif command == '1':
            sumOfSeries = sum_by_amount_of_terms(x)
            break
    print('Сумма ряда равна:\n', sumOfSeries)
