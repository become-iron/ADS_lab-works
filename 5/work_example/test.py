# -*- coding: utf-8 -*-

# переход на уровень выше для поиска модуля
import sys
sys.path.append('..\\')

from condition import check_condition

FILE_STRING = 'triplex_string.txt'  # имя файла с трипл. строкой
FILE_STRING_FROM_DB = 'triplex_string_from_DB.txt'
FILE_COND = 'conditions.txt'  # имя файла с условиями

trpString = open(FILE_STRING, 'r', encoding='utf-8').read()  # трипл. строка
trpStringFromDB = open(FILE_STRING_FROM_DB, 'r', encoding='utf-8').read()  # трипл. строка из базы данных
conditions = open(FILE_COND, 'r', encoding='utf-8').read().split('\n')  # условия
results = [check_condition(trpString, condition, trpStringFromDB) for condition in conditions]  # результаты проверки условий

print('Исходная триплексная строка:', trpString, sep='\n', end='\n\n')
if len(FILE_STRING_FROM_DB) > 0:
    print('Исходная триплексная строка из базы данных:', trpStringFromDB, sep='\n', end='\n\n')
print('Условия:', *conditions, sep='\n', end='\n\n')
print('Результаты проверки условий:', *results, sep='\n')
