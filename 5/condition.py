# -*- coding: utf-8 -*-
"""
Лабораторная работа №5. Вариант 2. «Реализация функции вычисления условия в правиле вывода»
Репозиторий: github.com/become-iron/ADS_lab-works/tree/master/5
"""

import re
from vsptd import Triplet, TriplexString, _BID, _RE_PREFIX_NAME2

# импортирование функций для реализации функции check_condition
from math import sin, cos, tan, acos, atan, sinh, cosh, tanh, sqrt, exp
from math import log as ln
from math import log10 as log

_RE_TRIPLET = re.compile('\$([A-Za-z])\.([A-Za-z]+)=([A-Za-zА-Яа-я0-9 \':\.]*);')  # триплет
_RE_FUNC_PRESENT = re.compile('(?:есть|ЕСТЬ)\(\$[A-Za-z]\.[A-Za-z]+\)')  # функция ЕСТЬ
_RE_FUNC_ABSENCE = re.compile('(?:нет|НЕТ)\(\$[A-Za-z]\.[A-Za-z]+\)')  # функция НЕТ


def strcat(a, b):
    return a + b


def check_condition(trpString, condition):
    # WARN используется опасный алгоритм, который также может не всегда верно работать
    """
    ПРОВЕРКА ТРИПЛЕКСНОЙ СТРОКИ НА УСЛОВИЕ
    Принимает:
        trpString (str) - триплексная строка
        condition (str) - условие
    Возвращает:
        (bool) - результат проверки условия
    Вызывает исключение ValueError, если:
        триплескная строка или условие не является строкой
        получена пустая строка вместо триплексной строки или условия
        триплет из условия не найден в триплексной строке
        в условии не соблюден баланс скобок
    """
    if not isinstance(trpString, str) or not isinstance(condition, str):
        raise ValueError('Триплексная строка и условие должны быть строками')
    if len(trpString) == 0 or len(condition) == 0:
        raise ValueError('Пустая строка или условие')

    # перевод трипл. строки из str в TriplexString
    trpString = re.findall(_RE_TRIPLET, trpString)
    tmpTrpString = []
    # определение типа значения
    for trp in trpString:
        if trp[2] in ('True', 'False'):  # булево значение
            value = bool(trp[2])
        elif trp[2].startswith('\'') and trp[2].endswith('\''):  # строка
            value = trp[2][1:-1]
        # elif trp[2].startswith('$') and trp[2].endswith(';'):  # TODO триплет
        #     pass
        elif trp[2] == _BID:  # заявка
            value = _BID
        else:  # число
            try:
                value = float(trp[2]) if '.' in trp[2] else int(trp[2])
            except ValueError:
                raise ValueError('Неверное значение триплета')
        tmpTrpString += [Triplet(trp[0], trp[1], value)]
    tmpTrpString = TriplexString(*tmpTrpString)
    trpString = tmpTrpString

    # WARN возможна неверная замена
    # например, замена слов произойдёт, даже если в условии происходит
    # сравнение со строкой, содержащей слово на замену
    # $W.B = ' или '
    replacements = [['или', 'or'],
                    ['и', 'and'],
                    ['ИЛИ', 'or'],
                    ['И', 'and'],
                    ['=', '=='],
                    ['<>', '!='],
                    ['^', '**']]
    for replacement in replacements:
        condition = condition.replace(replacement[0], replacement[1])

    # переводим названия функций в нижний регистр
    func_replacements = ['sin', 'cos', 'tan', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
                         'sqrt', 'exp', 'ln', 'log', 'strcat', 'min', 'max', 'abs']
    for replacement in func_replacements:
        condition = condition.replace(replacement.upper(), replacement)

    # замены для функций ЕСТЬ и НЕТ
    for trp in re.findall(_RE_FUNC_PRESENT, condition):  # функция ЕСТЬ
        item = trp[6:-1].upper().split('.')  # извлекаем префикс и имя в кортеж
        value = False
        for triplet in trpString.triplets:
            if [triplet.prefix, triplet.name] == item:
                value = True
                break
        condition = condition.replace(trp, str(value))
    for trp in re.findall(_RE_FUNC_ABSENCE, condition):  # функция НЕТ
        item = trp[5:-1].upper().split('.')  # извлекаем префикс и имя в кортеж
        value = False
        for triplet in trpString.triplets:
            if [triplet.prefix, triplet.name] == item:
                value = True
                break
        condition = condition.replace(trp, str(not value))

    for trp in re.findall(_RE_PREFIX_NAME2, condition):  # замена триплетов на их значения
        value = trpString.__getitem__(trp[1:])  # получаем значение триплета
        if value is None:
            raise ValueError('Триплет {} не найден'.format(trp))
        value = '\'{}\''.format(value) if isinstance(value, str) else str(value)  # приводим к формату значений триплета
        condition = condition.replace(trp, value)

    # проверка баланса скобок
    if condition.count('(') != condition.count(')'):
        raise ValueError('Не соблюден баланс скобок')

    # print('Конечное выражение: ', condition, sep='')
    return eval(condition)
