# -*- coding: utf-8 -*-
import re
from math import sin, cos, tan, acos, atan, sinh, cosh, tanh, sqrt
from math import log as ln
from math import log10 as log


_RE_PREFIX = re.compile('^[A-Za-z]$')  # префикс: 1 латинский символ
_RE_NAME = re.compile('^[A-Za-z]+$')  # имя: латинские символы
_RE_VALUE = re.compile('^[A-Za-zА-Яа-я0-9]*$')  # значение
_RE_PREFIX_NAME = re.compile('^[A-Za-z]\.[A-Za-z]+$')  # префикс.имя
_RE_PREFIX_NAME2 = re.compile('\$[A-Za-z]\.[A-Za-z]+')  # $префикс.имя


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


def is_in(a, b):
    return b in a


def is_not_in(a, b):
    return not (b in a)


class Triplet:
    """
    ТРИПЛЕТ
        Prefix - префикс
        Name - имя параметра
        Value - значение параметра
    """
    def __init__(self, prefix, name, value=''):
        if not isinstance(prefix, str):
            raise ValueError('Неверный формат данных. Должна быть строка')
        if not isinstance(name, str):
            raise ValueError('Неверный формат данных. Должна быть строка')
        if not isinstance(value, (str, int, float, Triplet)):
            raise ValueError('Неверный формат данных. Должна быть строка, число или триплексная строка')
        if re.match(_RE_PREFIX, prefix) is None:
            raise ValueError('Неверный вид префикса триплета')
        if re.match(_RE_NAME, name) is None:
            raise ValueError('Неверный вид имени триплета')
        # if re.match(_RE_VALUE, value) is None:  # TODO может быть и не строка
        #     raise ValueError
        # префикс и имя приводятся к верхнему регистру
        self.prefix = prefix.upper()
        self.name = name.upper()
        self.value = value

    def __str__(self):
        _ = '${}.{}='.format(self.prefix, self.name)
        if isinstance(self.value, str):
            _ += '\'{}\''.format(self.value)
        else:
            _ += str(self.value)
        _ += ';'
        return _

    def __add__(self, other):
        if isinstance(other, Triplet):
            return TripletString(self, other)
        if isinstance(other, TripletString):
            return TripletString(self, *other)
        else:
            raise ValueError

    def __eq__(self, other):
        return self.name == other.name and self.prefix == other.prefix and self.value == other.value


class TripletString:
    def __init__(self, *triplets):
        for _ in triplets:   # CHECK проверить скорость работы через filter
            if not isinstance(_, Triplet):
                raise ValueError('Аргументы должны быть триплетами')
        if len(triplets) > 0:
            self.trpString = triplets
        else:
            self.trpString = []

    def __len__(self):
        return len(self.trpString)

    # def __add__(self, other):
    #     if isinstance(other, Triplet):
    #         return TripletString(*([_ for _ in self.trpString] + [other]))  # TODO новый элемент вставляется в начало трипл. строки
    #     elif isinstance(other, TripletString):
    #         return TripletString(*([_ for _ in self.trpString] + [_ for _ in other]))  # WARN CHECK TODO новый элемент вставляется в начало трипл. строки, не совсем понятна работа
    #     else:
    #         raise ValueError

    def __str__(self):
        return ''.join(tuple(str(triplet) for triplet in self.trpString))

    def __contains__(self, item):
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
                return TripletString(*[self.trpString[i] for i in range(len(self.trpString)) if self.trpString[i].prefix == key])
            elif re.match(_RE_PREFIX_NAME, key) is not None:  # получить значение по префиксу и имени
                key = key.upper().split('.')
                for i in range(len(self.trpString)):
                    if self.trpString[i].prefix == key[0] and self.trpString[i].name == key[1]:
                        return self.trpString[i].value
                return None
            else:
                raise ValueError
        else:  # элемент по срезу
            return self.trpString[key]

    def __iter__(self):
        return iter(self.trpString)

    def del_trp(self, item):  # CHECK
        """Удалить триплет из триплексной строки
        """
        if not isinstance(item, Triplet):
            raise ValueError('Должен быть триплет')

        for i in range(len(self.trpString)):
            if self.trpString[i].prefix == item.prefix and \
               self.trpString[i].name == item.name and \
               self.trpString[i].value == item.value:
                del(self.trpString[i])
                return self
        return self

    def del_trp_pref(self, prefix):
        """Удалить все триплеты с заданным префиксом из триплексной строки
        """
        if not isinstance(prefix, str):
            raise ValueError('Должен быть триплет')

        for i in range(len(self.trpString)):
            if self.trpString[i].prefix == prefix:
                del(self.trpString[i])
        return self

    def check_condition(self, condition):
        """
        ПРОВЕРКА ТРИПЛ. СТРОКИ НА УСЛОВИЕ
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
                        [' <> ', ' != ']]
        for _ in replacements:
            condition = condition.replace(_[0], _[1])
            condition = condition.replace(_[0].upper(), _[1])  # для верхнего регистра

        # замены для ЕСТЬ и НЕТ
        # TODO
        # 1. оптимизировать
        # 2. заменить регулярки на вменяемые
        for _ in re.findall(r'есть\(\$[A-Za-z]\.[A-Za-z]+\)', condition) + re.findall(r'ЕСТЬ\(\$[A-Za-z]\.[A-Za-z]+\)', condition):
            item = _[6:-1].upper().split('.')
            val = False
            for triplet in self.trpString:
                if triplet.prefix == item[0] and triplet.name == item[1]:
                    val = True
                    break
            if val is True:
                condition = condition.replace(_, 'True')
            else:
                condition = condition.replace(_, 'False')
        for _ in re.findall(r'нет\(\$[A-Za-z]\.[A-Za-z]+\)', condition) + re.findall(r'НЕТ\(\$[A-Za-z]\.[A-Za-z]+\)', condition):
            item = _[5:-1].upper().split('.')
            val = False
            for triplet in self.trpString:
                if triplet.prefix == item[0] and triplet.name == item[1]:
                    val = True
                    break
            if val is True:
                condition = condition.replace(_, 'False')
            else:
                condition = condition.replace(_, 'True')

        for _ in re.findall(_RE_PREFIX_NAME2, condition):  # замена триплетов на их значения
            val = self.__getitem__(_[1:])
            if isinstance(val, str):  # е. значение триплета - строка, оборачиваем его в кавычки
                val = '"' + str(val) + '"'
            elif val is True:
                val = 'True'
            elif val is False:
                val = 'False'
            condition = condition.replace(_, val)
        print('Конечное выражение:\n', condition, '\n', sep='')
        return eval(condition)
