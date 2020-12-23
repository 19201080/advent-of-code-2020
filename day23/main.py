#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_input(filename):
    with open(filename, 'r') as f:
        return [int(el) for el in f.read()]


def dict_rounds(content, curr, rounds=100):
    max_keys = sorted(list(content.keys()))[-4:]
    for i in range(rounds):
        if not i % 1000000:
            print(f'round: {i}')
        three_cups = [cup := content[curr], cup := content[cup], content[cup]]
        dest = max({curr - i for i in range(1, 5)} - set(three_cups))
        if dest < 1:
            dest = max(set(max_keys) - set(three_cups))
        content[curr] = content[three_cups[-1]]
        content[three_cups[-1]] = content[dest]
        content[dest] = three_cups[0]
        curr = content[curr]
    return content


def make_linked_list(content):
    length = len(content)
    return {el: content[(idx + 1) % length]
            for idx, el in enumerate(content)}


def make_big_list(content, length=1000000):
    max_item = max(content) + 1
    return content[:] + list(range(max_item, length - len(content) + max_item))


def main():
    file_content = get_input('input')
    print(file_content)

    first = file_content[0]
    linked_content = make_linked_list(file_content)
    linked_result = dict_rounds(linked_content, first)
    result = [linked_result[1]]
    while len(result) < 8:
        result.append(linked_result[result[-1]])
    result = ''.join(str(el) for el in result)
    print(f'problem 1 - the solution is: {result}')

    linked_content = make_linked_list(make_big_list(file_content))
    linked_result = dict_rounds(linked_content, first, 10000000)
    result = linked_result[1]
    result *= linked_result[result]
    print(f'problem 2 - the solution is: {result}')


if __name__ == '__main__':
    main()
