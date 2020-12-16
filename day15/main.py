#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from time import time


def get_content(name):
    with open(name, 'r') as file:
        return [int(el) for el in file.read().strip().split(',')]


def process_data(content, turns=2020):
    cache = defaultdict(tuple, {v: (i+1,) for i, v in enumerate(content)})
    last = content[-1]
    for i in range(len(content), turns):
        rounds = cache[last]
        last = 0 if len(rounds) < 2 else rounds[1] - rounds[0]
        cache[last] = cache[last][-1:] + (i+1,)
    return last


if __name__ == '__main__':
    file_content = get_content('input')
    start = time()
    result = process_data(file_content)
    print(f'problem 1 - the solution is: {result} (time: {time() - start:5f})')

    start = time()
    result = process_data(file_content, 30000000)
    print(f'problem 2 - the solution is: {result} (time: {time() - start:5f})')
