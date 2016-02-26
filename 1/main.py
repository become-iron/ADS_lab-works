# -*- coding: utf-8 -*-
"""
Вычислить выражение: [см. приложенное изображение]
"""

from math import factorial, fabs  # высчитывание факториала, модуля числа
from decimal import Decimal  # для точных расчётов

sum_of_series = 1  # сумма ряда, включая первый его член равный 1
x = int(input('Задайте величину x\n'))
while True:
    accuracy = int(input('С какой точностью посчитать ряд (знаков после запятой)? (максимально 27)\n'))
    if accuracy <= 27:  # ограничение точности в связи с работой модуля decimal
        break


def n_term(n):
    """Высчитывание n-го члена ряда"""
    return Decimal(((-1) ** n) * (x ** (2 * n)) / factorial(2 * n))


i = 0
while True:
    i += 1
    _ = n_term(i)  # значение n-го члена ряда
    if fabs(_) < 10 ** (-accuracy):  # если значение n-го члена ряда меньше требуемой точности, завершить высчитывание
        break
    sum_of_series = Decimal(sum_of_series + _)
print('Сумма ряда равна:\n', sum_of_series)
