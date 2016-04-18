# -*- coding: utf-8 -*-

import re
from math import sin, cos, tan, acos, atan, sinh, cosh, tanh, sqrt
from math import log as ln
from math import log10 as log

_BID = ':'  # заявка (запрос полной информации по заданному объекту, определяемому префиксом)

_RE_PREFIX = re.compile('^[A-Za-z]$')  # префикс: 1 латинский символ
_RE_NAME = re.compile('^[A-Za-z]+$')  # имя: латинские символы
_RE_VALUE = re.compile('^[A-Za-zА-Яа-я0-9]*$')  # значение
_RE_PREFIX_NAME = re.compile('^[A-Za-z]\.[A-Za-z]+$')  # префикс.имя
_RE_PREFIX_NAME2 = re.compile('\$[A-Za-z]\.[A-Za-z]+')  # $префикс.имя
_RE_FUNC_PRESENT = re.compile('(?:есть|ЕСТЬ)\(\$[A-Za-z]\.[A-Za-z]+\)')  # функция ЕСТЬ
_RE_FUNC_ABSENCE = re.compile('(?:нет|НЕТ)\(\$[A-Za-z]\.[A-Za-z]+\)')  # функция НЕТ


# def parse_to_triplets(string='', file=None, count=-1):
#     """Парсинг строки/файла в триплеты
#     """
#     if file is not None:
#         pass
#     elif isinstance(string, str):
#         pass
#     else:
#         raise ValueError


def strcat(a, b):
    return a + b


class Triplet:
    """
    ТРИПЛЕТ
    Принимает:
        Prefix (str) - префикс (1 латинский символ)
        Name (str) - имя параметра (латинские символы)
        Value - значение параметра
    """
    def __init__(self, prefix, name, value=''):
        if not isinstance(prefix, str):
            raise ValueError('Префикс должен быть строкой')
        if not isinstance(name, str):
            raise ValueError('Имя должно быть строкой')
        if not isinstance(value, (str, int, float, Triplet, TriplexString)):
            raise ValueError('Значение должно быть строкой, числом, триплетом или триплексной строкой')
        if re.match(_RE_PREFIX, prefix) is None:
            raise ValueError('Неверный формат префикса')
        if re.match(_RE_NAME, name) is None:
            raise ValueError('Неверный формат имени')
        # TODO может быть и не строкой (следует уточнить)
        if isinstance(value, str) and value != _BID and re.match(_RE_VALUE, value) is None:
            raise ValueError

        # префикс и имя приводятся к верхнему регистру
        self.prefix = prefix.upper()
        self.name = name.upper()
        self.value = value

    def __str__(self):
        _ = '${}.{}='.format(self.prefix, self.name)
        if self.value == _BID:
            _ += _BID
        elif isinstance(self.value, str):
            _ += '\'{}\''.format(self.value)
        else:
            _ += str(self.value)
        _ += ';'
        return _

    def __add__(self, other):
        if isinstance(other, Triplet):
            return TriplexString(self, other)
        if isinstance(other, TriplexString):
            return TriplexString(self, *other)
        else:
            raise ValueError

    def __eq__(self, other):
        return isinstance(other, Triplet) and \
               self.name == other.name and \
               self.prefix == other.prefix and \
               self.value == other.value


class TriplexString:
    """
    ТРИПЛЕКСНАЯ СТРОКА
    Принимает:
        *triplets (Triplet) - триплеты
    """
    def __init__(self, *triplets):
        for _ in triplets:  # CHECK проверить скорость работы через filter
            if not isinstance(_, Triplet):
                raise ValueError('Аргументы должны быть триплетами')
        self.trpString = list(triplets)

        # удаление повторов триплетов (по префиксам и именам)
        trpString_copy = self.trpString.copy()
        for triplet in trpString_copy:
            # триплеты с данными префиксами и именами
            triplets_to_remove = [_ for _ in self.trpString if _.prefix == triplet.prefix and _.name == triplet.name]
            triplets_to_remove = triplets_to_remove[:-1]  # исключение последнего найденного триплета
            for secTriplet in triplets_to_remove:
                self.trpString.remove(secTriplet)

    def __len__(self):
        return len(self.trpString)

    def __add__(self, other):
        # CHECK
        if isinstance(other, Triplet):
            return TriplexString(*(self.trpString + [other]))
        elif isinstance(other, TriplexString):
            return TriplexString(*(self.trpString + other.trpString))
        else:
            raise ValueError

    def __str__(self):
        return ''.join(tuple(str(triplet) for triplet in self.trpString))

    def __contains__(self, item):
        # TODO возможно, стоит включить возможность проверки включения по префиксу и имени
        if not isinstance(item, Triplet):
            raise ValueError('Должен быть триплет')

        for triplet in self.trpString:
            if triplet.prefix == item.prefix and triplet.name == item.name and triplet.value == item.value:
                return True
        return False

    def __getitem__(self, key):
        # TODO CHECK
        if isinstance(key, str):  # элемент по ключу
            if re.match(_RE_PREFIX, key) is not None:  # получить триплеты по префиксу в виде триплесной строки
                return TriplexString(*[triplet for triplet in self.trpString if triplet.prefix == key])
            elif re.match(_RE_PREFIX_NAME, key) is not None:  # получить значение по префиксу и имени
                key = key.upper().split('.')
                for triplet in self.trpString:
                    if triplet.prefix == key[0] and triplet.name == key[1]:
                        return triplet.value
                return None
            else:
                raise ValueError('Неверный формат данных')
        else:  # элемент по срезу
            return self.trpString[key]

    def __eq__(self, other):
        # CHECK возможно, стоит замерить скорость работы
        if not isinstance(other, TriplexString):
            raise ValueError

        if len(self.trpString) != len(other):
            return False
        for triplet in other:
            if triplet not in self.trpString:
                return False
        return True

    def __iter__(self):
        return iter(self.trpString)

    def add(self, other):
        """
        СЛОЖЕНИЕ ТРИПЛЕКСНОЙ СТРОКИ С ТРИПЛЕКСНОЙ СТРОКОЙ ИЛИ ТРИПЛЕТОМ
        Эквивалентно сложению через оператор "+"
        Принимает:
            other (TriplexString или Triplet) - триплексная строка или триплет
        Возвращает:
            (TriplexString)
        """
        return self.__add__(other)

    def del_trp(self, prefix, name):
        # CHECK
        """
        УДАЛИТЬ ТРИПЛЕТ ИЗ ТРИПЛЕКСНОЙ СТРОКИ
        Принимает:
            item (Triplet) - триплет на удаление
        Вызывает исключение ValueError, если триплет не найден
        """
        if not isinstance(prefix, str):
            raise ValueError('Префикс должен быть строкой')
        if not isinstance(name, str):
            raise ValueError('Имя должно быть строкой')
        if re.match(_RE_PREFIX, prefix) is None:
            raise ValueError('Неверный формат префикса')
        if re.match(_RE_NAME, name) is None:
            raise ValueError('Неверный формат имени')

        for triplet in self.trpString:
            if triplet.prefix == prefix and triplet.name == name:
                self.trpString.remove(triplet)
                return
        raise ValueError('Триплет не найден')

    def del_trp_pref(self, prefix):
        # CHECK
        """
        УДАЛИТЬ ВСЕ ТРИПЛЕТЫ С ЗАДАННЫМ ПРЕФИКСОМ ИЗ ТРИПЛЕКСНОЙ СТРОКИ
        Принимает:
            prefix (str) - префикс
        """
        if not isinstance(prefix, str):
            raise ValueError('Должен быть триплет')

        for triplet in self.trpString:
            if triplet.prefix == prefix:
                self.trpString.remove(triplet)

    def check_condition(self, condition):
        # WARN используется опасный алгоритм, который также может не всегда верно работать
        """
        ПРОВЕРКА ТРИПЛЕКСНОЙ СТРОКИ НА УСЛОВИЕ
        Принимает:
            condition (str) - условие
        Возвращает:
            (bool) - результат проверки условия
        """
        if not isinstance(condition, str):
            raise ValueError('Должна быть строка')

        # WARN возможна неверная замена
        # например, замена слов произойдёт, даже если в условии происходит
        # сравнение со строкой, содержащей слово на замену
        # $W.B = " или "
        replacements = [[' или ', ' or '],
                        [' и ', ' and '],
                        [' = ', ' == '],
                        [' <> ', ' != '],
                        [' ^ ', ' ** ']]
        for _ in replacements:
            condition = condition.replace(_[0], _[1])
            condition = condition.replace(_[0].upper(), _[1])  # для верхнего регистра

        # замены для ЕСТЬ и НЕТ
        # TODO оптимизировать
        for _ in re.findall(_RE_FUNC_PRESENT, condition):  # функция ЕСТЬ
            item = _[6:-1].upper().split('.')
            val = False
            for triplet in self.trpString:
                if triplet.prefix == item[0] and triplet.name == item[1]:
                    val = True
                    break
            condition = condition.replace(_, str(val))
        for _ in re.findall(_RE_FUNC_ABSENCE, condition):  # функция НЕТ
            item = _[5:-1].upper().split('.')
            val = False
            for triplet in self.trpString:
                if triplet.prefix == item[0] and triplet.name == item[1]:
                    val = True
                    break
            condition = condition.replace(_,
                                          'False' if val is True else 'True')

        for _ in re.findall(_RE_PREFIX_NAME2, condition):  # замена триплетов на их значения
            val = self.__getitem__(_[1:])
            if isinstance(val, str):  # е. значение триплета - строка, оборачиваем его в кавычки
                val = '"{}"'.format(str(val))
            elif isinstance(val, bool):
                val = str(val)
            else:
                val = str(val)
            condition = condition.replace(_, val)

        # print('Конечное выражение:\n', condition, '\n', sep='')
        return eval(condition)
