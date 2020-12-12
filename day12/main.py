#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_content(name):
    with open(name, 'r') as file:
        content = [(el[0], int(el[1:])) for el in file.read().strip().split('\n')]
        return content


def rotate(start, angle, direction):
    quadrants = ['N', 'E', 'S', 'W']
    direction = 1 if direction == 'R' else -1
    angle = (angle // 90) * direction
    index = quadrants.index(start) + angle
    return quadrants[index % len(quadrants)]


instructions = {
    'N': lambda param, boat, direction:
        ([boat[0] + param, boat[1]], direction),
    'S': lambda param, boat, direction:
        ([boat[0] - param, boat[1]], direction),
    'E': lambda param, boat, direction:
        ([boat[0], boat[1] + param], direction),
    'W': lambda param, boat, direction:
        ([boat[0], boat[1] - param], direction),
    'L': lambda param, boat, direction:
        ([boat[0], boat[1]], rotate(direction, param, 'L')),
    'R': lambda param, boat, direction:
        ([boat[0], boat[1]], rotate(direction, param, 'R')),
    'F': lambda param, boat, direction:
        instructions[direction](param, boat, direction),
}


def run_instructions(content, direction='E'):
    boat = [0, 0]
    for op, param in content:
        boat, direction = instructions[op](param, boat, direction)
    return boat


def wp_rotate(wp, angle, direction):
    new_wp = [wp[(idx+angle//90) % len(wp)] for idx, _ in enumerate(wp)]
    if (angle // 90) % 2:
        new_wp[direction == 'L'] *= -1
    if (angle // 180) % 2:
        new_wp = [el * -1 for el in new_wp]
    return new_wp


waypoint_instructions = {
    'N': lambda param, boat, wp, direction:
        (boat, [wp[0] + param, wp[1]], direction),
    'S': lambda param, boat, wp, direction:
        (boat, [wp[0] - param, wp[1]], direction),
    'E': lambda param, boat, wp, direction:
        (boat, [wp[0], wp[1] + param], direction),
    'W': lambda param, boat, wp, direction:
        (boat, [wp[0], wp[1] - param], direction),
    'L': lambda param, boat, wp, direction:
        (boat, wp_rotate(wp, param, 'L'), direction),
    'R': lambda param, boat, wp, direction:
        (boat, wp_rotate(wp, param, 'R'), direction),
    'F': lambda param, boat, wp, direction:
        ([el + wp[idx] * param for idx, el in enumerate(boat)], wp, direction)
}


def run_waypoint_instructions(content, direction='E', wp_north=1, wp_east=10):
    boat = [0, 0]
    waypoint = [wp_north, wp_east]
    for op, param in content:
        boat, waypoint, direction = waypoint_instructions[op](
            param, boat, waypoint, direction)
    return boat


if __name__ == '__main__':
    file_content = get_content('input')

    north, east = run_instructions(file_content)
    result = abs(north) + abs(east)
    print(f'problem 1 - the solution is: {result}')

    north, east = run_waypoint_instructions(file_content)
    result = abs(north) + abs(east)
    print(f'problem 2 - the solution is: {result}')
