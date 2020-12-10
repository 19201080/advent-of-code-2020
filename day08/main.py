#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_content(name):
    with open(name, 'r') as file:
        content = file.read().strip().split('\n')
        content = [rule.split() for rule in content]
        return content


operations = {
    'acc': lambda arg, idx, acc: (idx + 1, acc + int(arg)),
    'jmp': lambda arg, idx, acc: (idx + int(arg), acc),
    'nop': lambda arg, idx, acc: (idx + 1, acc)
}


def run_operations(content, acc=0):
    indexes = []
    next_idx = 0
    while next_idx not in indexes and next_idx < len(content):
        indexes.append(next_idx)
        op, arg = content[next_idx]
        next_idx, acc = operations[op](arg, next_idx, acc)
    return next_idx, acc


def switch_and_run(content, switch):
    for index, (op, arg) in enumerate(content):
        if op in switch:
            op = switch[op == switch[0]]
            content_copy = content[:]
            content_copy[index] = [op, arg]
            last_idx, acc = run_operations(content_copy)
            if last_idx >= len(content):
                return acc
    return 'not found'


if __name__ == '__main__':
    file_content = get_content('input')
    _, result = run_operations(file_content)
    print(f'problem 1 - the solution is: {result}')

    result = switch_and_run(file_content, ('jmp', 'nop'))
    print(f'problem 2 - the solution is: {result}')
