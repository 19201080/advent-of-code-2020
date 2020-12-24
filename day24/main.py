#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import re


def get_input(filename):
    with open(filename, 'r') as f:
        return f.read().split('\n')


def get_directions(content):
    return [re.findall(r'([ns]?[ew])', line) for line in content]


def get_coords(content):
    options = {'nw': (1, -1), 'w': (0, -2), 'sw': (-1, -1),
               'ne': (1, 1), 'e': (0, 2), 'se': (-1, 1)}
    return [[options[coord] for coord in line] for line in content]


def get_positions(content):
    zipped = [list(zip(*line)) for line in content]
    return [(sum(line[0]), sum(line[1])) for line in zipped]


def get_colors(content):
    occurrences = defaultdict(int)
    for tile in content:
        occurrences[tile] += 1
    return {k: v % 2 for k, v in occurrences.items()}


def run_days(content, days=100):
    def run_a_day(tile, color, all_tiles):
        adjacent = [(1, -1), (0, -2), (-1, -1), (1, 1), (0, 2), (-1, 1)]
        neighbors = [(tile[0] + el[0], tile[1] + el[1]) for el in adjacent]
        new_neighbors = [item for item in neighbors if item not in all_tiles]
        black_neighbors = sum([all_tiles.get(tile, 0) for tile in neighbors])
        if color and black_neighbors not in (1, 2):
            return 0, new_neighbors
        if not color and black_neighbors == 2:
            return 1, new_neighbors
        return color, new_neighbors

    content = get_colors(get_positions(get_coords(get_directions(content))))

    for i in range(days):
        new_content = {k: run_a_day(k, v, content) for k, v in content.items()}
        new_tiles = {el: run_a_day(el, 0, content)[0]
                     for v in new_content.values() for el in v[1]}
        content = {**{k: v[0] for k, v in new_content.items()}, **new_tiles}
    return len([k for k, v in content.items() if v])


def main():
    file_content = get_input('input')
    result = run_days(file_content, 0)
    print(f'problem 1 - the solution is: {result}')
    result = run_days(file_content)
    print(f'problem 2 - the solution is: {result}')


if __name__ == '__main__':
    main()
