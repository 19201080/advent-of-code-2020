#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from copy import deepcopy

ACTIVE = '#'
INACTIVE = '.'


def get_content(name):
    with open(name, 'r') as file:
        return {(x_idx, y_idx, 0): x
                for y_idx, y in enumerate(file.read().strip().split('\n'))
                for x_idx, x in enumerate(y)}


def do_round(content, dimensions):
    active_cubes = []
    for k, v in content.items():
        if v == ACTIVE:
            active_cubes.append(k)
    step = [-1, 0, 1]
    if dimensions == 3:
        directions = [(x, y, z)
                      for x in step for y in step for z in step
                      if x or y or z]
    else:
        directions = [(x, y, z, w)
                      for x in step for y in step for z in step for w in step
                      if x or y or z or w]
    neighbors = [[cube[idx] + direction[idx] for idx, el in enumerate(cube)]
                 for cube in active_cubes for direction in directions]
    counted = defaultdict(int)
    for location in neighbors:
        counted[tuple(location)] += 1
    neighbors = {k: v for k, v in counted.items() if 1 < v < 4}
    new_actives = [k for k, v in neighbors.items() if k in active_cubes]
    new_actives += [k for k, v in neighbors.items()
                    if v == 3 and k not in active_cubes]
    return new_actives


def update_cube(actives):
    result = {location: ACTIVE for location in actives}
    return result


def run_rounds(content, rounds, dimensions=3):
    new_content = deepcopy(content)
    total_actives = 0
    for i in range(rounds):
        new_actives = do_round(new_content, dimensions)
        new_content = update_cube(new_actives)
        total_actives = sum(el == ACTIVE for el in new_content.values())
    return total_actives


def main():
    file_content = get_content('input')
    result = run_rounds(file_content, 6)
    print(f'problem 1 - the solution is: {result}')

    four_dimensions = {k + (0,): v for k, v in file_content.items()}
    result = run_rounds(four_dimensions, 6, 4)
    print(f'problem 2 - the solution is: {result}')


if __name__ == '__main__':
    main()
