#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_content(name):
    with open(name, 'r') as file:
        content = file.read().strip().split('\n')
        return content


def compute(content, down_incr, right_incr, symbol):
    filtered = [line for index, line in enumerate(content) 
                if index % down_incr == 0]
    results = [line[(index*right_incr) % len(line)] 
               for index, line in enumerate(filtered)]
    return len([el for el in results if el == symbol])


def multiply_list(content):
    result = 1
    for el in content:
        result *= el
    return result


if __name__ == '__main__':
    content = get_content('input')
    trajectories = ((1, 1), (1, 3), (1, 5), (1, 7), (2, 1))
    results = [compute(content, el[0], el[1], '#') for el in trajectories]
    result = multiply_list(results)
    print(f'problem 1 - the solution is: {results[1]}')
    print(f'problem 2 - the solution is: {result}')
