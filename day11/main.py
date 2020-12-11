#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy

FLOOR = '.'
EMPTY_SEAT = 'L'
OCCUPIED_SEAT = '#'


def get_content(name):
    with open(name, 'r') as file:
        content = [list(el) for el in file.read().strip().split('\n')]
        return content


def flat(content):
    return [item for sublist in content for item in sublist]


def get_seat(seat_idx, line_idx, layout):
    if seat_idx >= 0 and line_idx >= 0:
        try:
            return layout[line_idx][seat_idx]
        except IndexError:
            pass


def get_adjacent_seats(seat_idx, line_idx, layout):
    directions = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if x or y]
    return [get_seat(seat_idx+x, line_idx+y, layout) for x, y in directions]


def get_next_seats(seat_idx, line_idx, layout):
    line_range = range(len(layout[line_idx]))
    layout_range = range(len(layout))
    next_seats = []
    directions = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if x or y]
    for x, y in directions:
        next_seat_idx = seat_idx + x
        next_line_idx = line_idx + y
        while next_seat_idx in line_range and next_line_idx in layout_range:
            if layout[next_line_idx][next_seat_idx] != FLOOR:
                next_seats.append(layout[next_line_idx][next_seat_idx])
                break
            else:
                next_seat_idx += x
                next_line_idx += y
    return next_seats


def switch_seat(seat, seat_index, line_index, layout, part):
    if seat == FLOOR:
        return seat

    if part == 1:
        adjacent_seats = get_adjacent_seats(seat_index, line_index, layout)
    else:
        adjacent_seats = get_next_seats(seat_index, line_index, layout)

    if seat == EMPTY_SEAT:
        if any(seat == OCCUPIED_SEAT for seat in adjacent_seats):
            return EMPTY_SEAT
        return OCCUPIED_SEAT

    if seat == OCCUPIED_SEAT:
        limit = 3 if part == 1 else 4
        if sum(seat == OCCUPIED_SEAT for seat in adjacent_seats) > limit:
            return EMPTY_SEAT
        return OCCUPIED_SEAT


def do_a_round(content, mode, part):
    return [[switch_seat(seat, seat_idx, line_idx, content, part)
             if seat == mode else seat for seat_idx, seat in enumerate(line)]
            for line_idx, line in enumerate(content)]


def run_rounds(content, part=1):
    old_results = []
    new_results = deepcopy(content)
    mode = [item for item in flat(content) if item != FLOOR][0]

    while old_results != new_results:
        new_results = do_a_round(old_results := new_results, mode, part)
        mode = OCCUPIED_SEAT if mode == EMPTY_SEAT else EMPTY_SEAT
    return new_results


if __name__ == '__main__':
    file_content = get_content('input')
    result = run_rounds(file_content)
    result = sum(seat == OCCUPIED_SEAT for seat in flat(result))
    print(f'problem 1 - the solution is {result}')

    result = run_rounds(file_content, part=2)
    result = sum(seat == OCCUPIED_SEAT for seat in flat(result))
    print(f'problem 2 - the solution is {result}')
