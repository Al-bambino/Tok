def inpt(tekst, type):
    if (type == 'int'):
        return int(input(tekst))
    if type == 'double':
        return float(input(tekst))
    if type == 'string':
        return input(tekst)


def spit(tekst):
    print(tekst)


def castStr(n):
    return str(n)


def randm(a, b):
    import random
    return random.randrange(a, b)


def sqrt(a):
    import math
    return math.sqrt(a)


def isIntg(a):
    return float.is_integer(a)


def strLen(a):
    return len(a)


def charAt(a, i):
    print(i)
    return a[i]


def isNumeric(a):
    return a.isnumeric()


def isAlpha(a):
    return a.isalpha()


def rround(a):
    return round(a)


def castInt(a):
    return int(a)


def strtupper(a):
    return a.upper()


def arr_get(a, i):
    return a[i]


def arr_push(a, i):
    return a.append(i)


def count(a):
    return len(a)
