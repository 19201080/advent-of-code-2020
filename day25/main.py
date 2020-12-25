#!/usr/bin/env python
# -*- coding: utf-8 -*-

MODULO = 20201227


def get_input(filename):
    with open(filename, 'r') as f:
        return [int(line) for line in f.read().split('\n')]


def transform(subject, loops):
    result = 1
    for _ in range(loops):
        result = (result * subject) % MODULO
    return result


def get_loop_size(key, sub_num):
    value = 1
    loop = 0
    while value != key:
        value = (value * sub_num) % MODULO
        loop += 1
    return loop


def main():
    card_key, door_key = get_input('input')
    result = transform(door_key, get_loop_size(card_key, 7))
    print(f'problem 1 - the solution is: {result}')


if __name__ == '__main__':
    main()
