#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_content(name):
    with open(name, 'r') as file:
        content = [int(el) for el in file.read().strip().split('\n')]
        return content


def get_non_compliant_number(content, preamble):
    for index, item in enumerate(content[preamble:]):
        sublist = content[index:index+preamble]
        combinations = [x + y for x in sublist for y in sublist if x != y]
        if item not in combinations:
            return item
    return 'not found'


def get_contiguous_elements(content, target):
    for index, element in enumerate(content):
        contiguous = [element]
        while sum(contiguous) < target:
            contiguous.append(content[len(contiguous) + index])
        if sum(contiguous) == target:
            return contiguous
    return 'not found'


if __name__ == '__main__':
    file_content = get_content('input')
    result = get_non_compliant_number(file_content, 25)
    print(f'problem 1 - the solution is: {result}')

    result = get_contiguous_elements(file_content, result)
    result = min(result) + max(result)
    print(f'problem 2 - the solution is: {result}')
