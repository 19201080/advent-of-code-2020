#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def get_content(name):
    with open(name, 'r') as file:
        content = file.read().strip().split('\n')
        return [re.findall(r'(\d+) (\w+\s\w+)', '1 ' + element)
                for element in content]


def get_bags_containing(content, target):
    prev_targets = {target} if isinstance(target, str) else target
    targets = {bags[0] for bags in content
               if any(t in bags[1:] for t in prev_targets)}
    if len(targets) > len(prev_targets):
        return get_bags_containing(content, targets | prev_targets)
    else:
        return targets


def get_bags_contained_in(content, bag_color):
    def get_children(target):
        if target is None:
            return {}
        else:
            return {bag: get_children(bag)
                    for rule in content for bag in rule[1:]
                    if target[1] in rule[0]}

    def get_amount(children):
        if not children:
            return 0
        else:
            return sum(int(key[0]) * (1 + get_amount(value))
                       for key, value in children.items())

    return get_amount(get_children((bag_color, bag_color)))


if __name__ == '__main__':
    file_content = get_content('input')
    without_numbers = [[bag[1] for bag in rule] for rule in file_content]
    results = len(get_bags_containing(without_numbers, 'shiny gold'))
    print(f'problem 1 - the solution is: {results}')

    results = get_bags_contained_in(file_content, 'shiny gold')
    print(f'problem 2 - the solution is: {results}')
