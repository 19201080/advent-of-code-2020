#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def get_content(name):
    with open(name, 'r') as file:
        content = file.read().strip().split('mask = ')[1:]
        content = [[el for el in sublist.split('\n') if el]
                   for sublist in content]
        content = [[[int(code) for code in re.findall(r'\d+', el)]
                    if el.startswith('mem') else el for el in part]
                   for part in content]
        return content


def get_bitmasked_values(content):
    def apply_bitmask(sequence):
        no_x = int(sequence[0].replace('X', '0'), 2)
        x_mask = int(sequence[0].replace('1', '0').replace('X', '1'), 2)
        bitmasked = [[element[0], element[1] & x_mask | no_x]
                     for element in sequence[1:]]
        return bitmasked
    return [apply_bitmask(sequence) for sequence in content]


def get_bitmasked_memory(content):
    def get_permutations(seq, indexes):
        if not indexes:
            return int(''.join(seq), 2)
        res = []
        for i in ('0', '1'):
            new_seq = seq[:]
            new_seq[indexes[0]] = i
            res.append(get_permutations(new_seq, indexes[1:]))
        return res

    def flatten(seq):
        if len(seq) == 0:
            return seq
        if isinstance(seq[0], list):
            return flatten(seq[0]) + flatten(seq[1:])
        return seq[:1] + flatten(seq[1:])

    def int_to_binary(number):
        return format(number, '36b').replace(' ', '0')

    def compute_sequence(seq):
        x_indexes = [idx for idx, el in enumerate(seq[0]) if el == 'X']
        mask = int(seq[0].replace('X', '0'), 2)
        bitmasked = [[list(int_to_binary(mem | mask)), val]
                     for mem, val in seq[1:]]
        return [[flatten(get_permutations(mem, x_indexes)), val]
                for mem, val in bitmasked]

    return [compute_sequence(sequence) for sequence in content]


def parse_part1_results(content):
    return sum({el[0]: el[1]
                for sequence in content for el in sequence}.values())


def parse_part2_results(content):
    return sum({mem: val for sequence in content
                for memories, val in sequence for mem in memories}.values())


if __name__ == '__main__':
    file_content = get_content('input')
    result = parse_part1_results(get_bitmasked_values(file_content))
    print(f'problem 1 - the solution is: {result}')
    result = parse_part2_results(get_bitmasked_memory(file_content))
    print(f'problem 2 - the solution is: {result}')
