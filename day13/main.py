#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import reduce
import math


def get_content(name):
    with open(name, 'r') as file:
        content = file.read().strip().split('\n')
        content[0] = int(content[0])
        content[1] = [int(el) if el != 'x' else el
                      for el in content[1].split(',')]
        return content


def get_earliest_bus(target, bus_ids):
    earliest = [[bus, bus * math.ceil(target/bus)]
                for bus in bus_ids if isinstance(bus, int)]
    earliest = sorted(earliest, key=lambda x: x[1])
    return earliest[0]


# code from: https://rosettacode.org/wiki/Chinese_remainder_theorem
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


def get_timestamp(bus_ids):
    bus_starts = [bus - idx for idx, bus in enumerate(bus_ids)
                  if isinstance(bus, int)]
    bus_ids = [bus for bus in bus_ids if isinstance(bus, int)]
    return chinese_remainder(bus_ids, bus_starts)


if __name__ == '__main__':
    file_content = get_content('input')
    bus_id, t = get_earliest_bus(*file_content)
    result = bus_id * (t - file_content[0])
    print(f'problem 1 - the result is: {result}')

    result = get_timestamp(file_content[1])
    print(f'problem 2 - the result is: {result}')
