#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def get_content(name):
    with open(name, 'r') as file:
        return file.read().strip().split('\n')


def string_to_binary(boarding_pass):
    result = re.sub(r'B|R', '1', boarding_pass)
    result = re.sub(r'F|L', '0', result)
    return result


def decode_boarding_pass(passes):
    as_binary = [string_to_binary(boarding_pass) for boarding_pass in passes]
    return [[int(boarding_pass[:7], 2), int(boarding_pass[-3:], 2)]
            for boarding_pass in as_binary]


def get_seat_id(passes):
    return [boarding_pass[0] * 8 + boarding_pass[1]
            for boarding_pass in passes]


def get_missing_seat(seats):
    return list(set(range(min(seats), max(seats) + 1)) - set(seats))[0]


if __name__ == '__main__':
    file_content = get_content('input')
    decoded_passes = decode_boarding_pass(file_content)
    seat_ids = get_seat_id(decoded_passes)
    highest_seat_id = max(seat_ids)
    print(f'problem 1 - the solution is: {highest_seat_id}')

    missing_seat = get_missing_seat(seat_ids)
    print(f'problem 1 - the solution is: {missing_seat}')
