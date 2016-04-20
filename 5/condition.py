# -*- coding: utf-8 -*-
import re
from vsptd import Triplet, TriplexString, _BID, _RE_PREFIX_NAME2

# импортирование функций для реализации функции check_condition
from math import sin, cos, tan, acos, atan, sinh, cosh, tanh, sqrt
from math import log as ln
from math import log10 as log


_RE_TRIPLET = re.compile('\$([A-Za-z])\.([A-Za-z]+)=([A-Za-zА-Яа-я0-9 \':]*);')  # триплет
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
    """
    if not isinstance(condition, str) or not isinstance(condition, str):
        raise ValueError('Триплексная строка и условие должны быть строками')

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
    replacements = [[' или ', ' or '],
                    [' и ', ' and '],
                    [' = ', ' == '],
                    [' <> ', ' != '],
                    [' ^ ', ' ** ']]
    for trp in replacements:
        condition = condition.replace(trp[0], trp[1])
        condition = condition.replace(trp[0].upper(), trp[1])  # для верхнего регистра

    # замены для ЕСТЬ и НЕТ
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
        value = trpString.__getitem__(trp[1:])
        if isinstance(value, str):  # е. значение триплета - строка, оборачиваем его в кавычки
            value = '"{}"'.format(str(value))
        elif isinstance(value, bool):
            value = str(value)
        else:
            value = str(value)
        condition = condition.replace(trp, value)

    # print('Конечное выражение: ', condition, sep='')
    return eval(condition)
