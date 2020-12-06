#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_content(name):
    with open(name, 'r') as file:
        content = file.read().strip().split('\n\n')
        content = [el.split('\n') for el in content]
        return [[list(el) for el in group] for group in content]


def get_unique_answers(content):
    return [set(group[0]).union(*group) for group in content]


def get_common_answers(content):
    return [set(group[0]).intersection(*group) for group in content]


def get_sublist_length(content):
    return [len(item) for item in content]


if __name__ == '__main__':
    file_content = get_content('input')
    results = sum(get_sublist_length(get_unique_answers(file_content)))
    print(f'problem 1 - the solution is: {results}')

    results = sum(get_sublist_length(get_common_answers(file_content)))
    print(f'problem 2 - the solution is: {results}')

