#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict


def get_input(filename):
    with open(filename, 'r') as f:
        content = [[items for items in line.split('(')]
                   for line in f.read().split('\n')]
        content = [[group[0].strip().split(' '), group[1][9:-1].split(', ')]
                   for group in content]
        return content


def get_food_without_allergens(content):
    all_ingredients = defaultdict(int)
    for item in content:
        for ingredient in item[0]:
            all_ingredients[ingredient] += 1

    dangerous = defaultdict(list)
    for ingredients, allergens in content:
        for allergen in allergens:
            dangerous[allergen].append(set(ingredients))
    dangerous = {k: set.intersection(*v) for k, v in dangerous.items()}

    while any(len(v) > 1 for v in dangerous.values()):
        to_be_removed = [(k, v) for k, v in dangerous.items() if len(v) < 2]
        for allergen, ingredient in to_be_removed:
            dangerous = {k: v - ingredient if k != allergen else v
                         for k, v in dangerous.items()}

    with_allergens = set.union(*[v for v in dangerous.values()])
    without_allergens = {k for k in all_ingredients.keys()} - with_allergens
    return (sum([all_ingredients[without] for without in without_allergens]),
            dangerous)


def get_canonical_list(dangerous):
    return ','.join([list(dangerous[key])[0] for key in sorted(dangerous)])


def main():
    file_content = get_input('input')
    result, dangerous = get_food_without_allergens(file_content)
    print(f'problem 1 - the solution is: {result}')

    result = get_canonical_list(dangerous)
    print(f'problem 2 - the solution is: {result}')


if __name__ == '__main__':
    main()
