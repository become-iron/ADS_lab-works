# -*- coding: utf-8 -*-
from condition import check_condition

FILE_STRING = 'triplex_string.txt'  # имя файла с трипл. строкой
FILE_COND = 'conditions.txt'  # имя файла с условием

trpString = open(FILE_STRING, 'r', encoding='utf-8').read()  # трипл. строка
conditions = open(FILE_COND, 'r', encoding='utf-8').read().split('\n')  # условия
results = [check_condition(trpString, condition) for condition in conditions]  # результаты проверки условий

print('Исходная триплексная строка:', trpString, sep='\n', end='\n\n')
print('Условия:', *conditions, sep='\n', end='\n\n')
print('Результаты проверки условий:', *results, sep='\n')
