#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def get_content(name):
    with open(name, 'r') as file:
        return [[int(el) if el.isnumeric() else el
                 for el in re.findall(r'(\d+|[^\s])', el)]
                for el in file.read().strip().split('\n')]


def base_operation(content, op):
    ops = {'+': lambda a, b: a + b,
           '*': lambda a, b: a * b}
    op_idx = [idx for idx, el in enumerate(content) if el == op][0]
    res = ops[op](content[op_idx-1], content[op_idx+1])
    return [*content[:op_idx-1], res, *content[op_idx+2:]]


def sequential_operations(content):
    new_content = content[:]
    while any(not isinstance(el, int) for el in new_content):
        next_op = [el for el in new_content if not isinstance(el, int)][0]
        new_content = base_operation(new_content, next_op)
    return new_content[0]


def complex_operations(content):
    new_content = content[:]
    for op in ['+', '*']:
        while any(el == op for el in new_content):
            new_content = base_operation(new_content, op)
    return new_content[0]


def process_line(line, mode):
    operation = sequential_operations if mode == 1 else complex_operations
    new_line = line[:]
    while any(el == ')' for el in new_line):
        closing_idx = [idx for idx, el in enumerate(new_line)
                       if el == ')'][0]
        opening_idx = [idx for idx, el in enumerate(new_line[:closing_idx])
                       if el == '('][-1]
        result = operation(new_line[opening_idx+1:closing_idx])
        new_line = [*new_line[:opening_idx], result, *new_line[closing_idx+1:]]
    return operation(new_line)


def process_content(content, mode=1):
    return sum(process_line(line, mode) for line in content)


def main():
    file_content = get_content('input')
    result = process_content(file_content)
    print(f'problem 1 - the solution is: {result}')
    result = process_content(file_content, 2)
    print(f'problem 2 - the solution is: {result}')


if __name__ == '__main__':
    main()
