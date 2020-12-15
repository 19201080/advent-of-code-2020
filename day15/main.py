#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_content(name):
    with open(name, 'r') as file:
        return [int(el) for el in file.read().strip().split(',')]


def process_data(content, rounds=2020):
    cache = {val: (idx+1,) for idx, val in enumerate(content)}
    data = content[:]
    for i in range(rounds - len(data)):
        last_rounds = cache.get(data[-1], ())
        data.append(last_number := 0 if len(last_rounds) < 2 else
                    last_rounds[-1] - last_rounds[-2])
        cache[last_number] = cache.get(last_number, ())[-1:] + (len(data),)
    return data[-1]


if __name__ == '__main__':
    file_content = get_content('input')
    result = process_data(file_content)
    print(f'problem 1 - the solution is: {result}')

    result = process_data(file_content, 30000000)
    print(f'problem 2 - the solution is: {result}')
