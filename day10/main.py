#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import reduce


def get_content(name):
    with open(name, 'r') as file:
        content = [int(el) for el in file.read().strip().split('\n')]
        return content


def get_differences(content):
    content = sorted(content)
    built_in = content[-1] + 3
    gaps = [b - a for a, b in zip([0, *content], [*content, built_in])]
    return (len([el for el in gaps if el == 1]),
            len([el for el in gaps if el == 3]),
            gaps)


def get_outcomes(content):
    def node_outcomes(size):
        if size < 2:
            return 1
        return sum(node_outcomes(size - item)
                   for item in range(1, size) if item <= 3)

    nodes = []
    node_size = 0
    for gap in content:
        if gap == 1:
            node_size += 1
        else:
            if node_size > 1:
                nodes.append(node_size)
            node_size = 0
    return reduce(lambda el, acc: el * acc,
                  [node_outcomes(node + 1) for node in nodes])


if __name__ == '__main__':
    file_content = get_content('input')
    ones, threes, gap_list = get_differences(file_content)
    result = ones * threes
    print(f'problem 1 - the solution is {result}')

    result = get_outcomes(gap_list)
    print(f'problem 2 - the solution is {result}')
