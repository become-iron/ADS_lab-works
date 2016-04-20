# -*- coding: utf-8 -*-
from condition import check_condition

FILE_NAME = 'input.txt'  # имя файла с трипл. строкой
FIlE_COND = 'cond.txt'  # имя файла с условием

exampleString = open(FILE_NAME, 'r').read()  # трипл. строка
condition = open(FIlE_COND, 'r').read()  # условие
result = check_condition(exampleString, condition)  # результат проверки условия

print('Исходная триплексная строка: \n', exampleString, '\n')
print('Условие: \n', condition, '\n')
print('Результат проверки условия: \n', result, '\n')
