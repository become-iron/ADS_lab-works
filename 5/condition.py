# -*- coding: utf-8 -*-
"""
Лабораторная работа №5. Вариант 2. «Реализация функции вычисления условия в правиле вывода»
Репозиторий: github.com/become-iron/ADS_lab-works/tree/master/5
"""

import re
from vsptd import Triplet, TriplexString, _BID, _RE_PREFIX_NAME, _RE_PREFIX_NAME_WODS

# импортирование функций для реализации функции check_condition
from math import sin, cos, tan, acos, atan, sinh, cosh, tanh, sqrt, exp
from math import log as ln
from math import log10 as log

_RE_TRIPLET = re.compile('\$([A-Za-z])\.([A-Za-z]+)=([A-Za-zА-Яа-я0-9 \':\.]*);')  # триплет
_RE_TRIPLET_WODS = re.compile('([A-Za-z])\.([A-Za-z]+)=([A-Za-zА-Яа-я0-9 \':\.]*);')  # триплет без $
_RE_FUNC_PRESENT = re.compile('(?:есть|ЕСТЬ)\(\$[A-Za-z]\.[A-Za-z]+\)')  # функция ЕСТЬ
_RE_FUNC_PRESENT_WODS = re.compile('(?:есть|ЕСТЬ)\([A-Za-z]\.[A-Za-z]+\)')  # функция ЕСТЬ без $
_RE_FUNC_ABSENCE = re.compile('(?:нет|НЕТ)\(\$[A-Za-z]\.[A-Za-z]+\)')  # функция НЕТ
_RE_FUNC_ABSENCE_WODS = re.compile('(?:нет|НЕТ)\([A-Za-z]\.[A-Za-z]+\)')  # функция НЕТ без $


def strcat(a, b):
    return a + b


def _parse_triplex_string(trpString):
    """ПАРСИНГ ТРИПЛЕКСНОЙ СТРОКИ ИЗ str В TriplexString"""
    trpString = re.findall(_RE_TRIPLET, trpString)
    tmpTrpString = []
    for trp in trpString:
        value = _determine_value(trp[2])
        tmpTrpString += [Triplet(trp[0], trp[1], value)]
    return TriplexString(*tmpTrpString)


def _determine_value(value):
    """ОПРЕДЕЛЕНИЕ ТИПА ЗНАЧЕНИЯ"""
    if value in ('True', 'False'):  # булево значение
        value = bool(value)
    elif value.startswith('\'') and value.endswith('\''):  # строка
        value = value[1:-1]
    # elif val.startswith('$') and val.endswith(';'):  # TODO триплет
    #     pass
    elif value == _BID:  # заявка
        value = _BID
    else:  # число
        try:
            value = float(value) if '.' in value else int(value)
        except ValueError:
            raise ValueError('Неверное значение триплета')
    return value


def check_condition(trpString, condition, trpStringFromDB=''):
    # WARN используется опасный алгоритм, который также может не всегда верно работать
    """
    ПРОВЕРКА ТРИПЛЕКСНОЙ СТРОКИ НА УСЛОВИЕ
    Принимает:
        trpString (str) - триплексная строка
        condition (str) - условие
        trpStringFromDB (str) необязательный - триплексная строка по данным из базы данных
    Возвращает:
        (bool) - результат проверки условия
    Вызывает исключение ValueError, если:
        триплескная строка или условие не является строкой
        получена пустая строка вместо триплексной строки или условия
        триплет из условия не найден в триплексной строке
        в условии не соблюден баланс скобок
    """
    if not isinstance(trpString, str) or not isinstance(trpStringFromDB, str):
        raise ValueError('Триплексная строка должна быть строкой')
    if not isinstance(condition, str):
        raise ValueError('Условие должно быть строкой')
    if len(trpString) == 0:
        raise ValueError('Пустая строка')
    if len(condition) == 0:
        raise ValueError('Пустое условие')

    trpString = _parse_triplex_string(trpString)
    trpStringFromDB = _parse_triplex_string(trpStringFromDB)

    # замена операторов
    # WARN возможна неверная замена
    # например, замена слов произойдёт, даже если в условии происходит
    # сравнение со строкой, содержащей слово на замену
    # $W.B = ' или '
    replacements = [[' или ', ' or '],
                    [' и ', ' and '],
                    [' ИЛИ ', ' or '],
                    [' И ', ' and '],
                    ['=', '=='],
                    ['<>', '!='],
                    ['^', '**']]
    for replacement in replacements:
        condition = condition.replace(replacement[0], replacement[1])

    # переводим названия функций в нижний регистр
    func_replacements = ('sin', 'cos', 'tan', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
                         'sqrt', 'exp', 'ln', 'log', 'strcat', 'min', 'max', 'abs')
    for replacement in func_replacements:
        condition = condition.replace(replacement.upper(), replacement)

    # замены для функций ЕСТЬ и НЕТ
    # TODO
    # поиск триплетов в строке
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
    # поиск триплетов в строке по данным из базы
    if len(trpStringFromDB) > 0:
        for trp in re.findall(_RE_FUNC_PRESENT_WODS, condition):  # функция ЕСТЬ
            item = trp[5:-1].upper().split('.')  # извлекаем префикс и имя в кортеж
            value = False
            for triplet in trpStringFromDB.triplets:
                if [triplet.prefix, triplet.name] == item:
                    value = True
                    break
            condition = condition.replace(trp, str(value))
        for trp in re.findall(_RE_FUNC_ABSENCE_WODS, condition):  # функция НЕТ
            item = trp[4:-1].upper().split('.')  # извлекаем префикс и имя в кортеж
            value = False
            for triplet in trpStringFromDB.triplets:
                if [triplet.prefix, triplet.name] == item:
                    value = True
                    break
            condition = condition.replace(trp, str(not value))

    # поиск триплетов
    for trp in re.findall(_RE_PREFIX_NAME, condition):  # замена триплетов на их значения
        value = trpString.__getitem__(trp[1:])  # получаем значение триплета
        if value is None:
            raise ValueError('Триплет {} не найден не найден в триплескной строке'.format(trp))
        value = '\'{}\''.format(value) if isinstance(value, str) else str(value)  # приводим к формату значений триплета
        condition = condition.replace(trp, value)
    # поиск триплетов в строке по данным из базы
    if len(trpStringFromDB) > 0:
        for trp in re.findall(_RE_PREFIX_NAME_WODS, condition):  # замена триплетов на их значения
            value = trpStringFromDB.__getitem__(trp)  # получаем значение триплета
            if value is None:
                raise ValueError('Триплет {} не найден в триплескной строке из базы'.format(trp))
            value = '\'{}\''.format(value) if isinstance(value, str) else str(value)  # приводим к формату значений триплета
            condition = condition.replace(trp, value)

    # проверка баланса скобок
    if condition.count('(') != condition.count(')'):
        raise ValueError('Не соблюден баланс скобок')

    # print('Конечное выражение: ', condition, sep='')
    return eval(condition)
