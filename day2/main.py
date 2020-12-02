#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def get_content(filename):
    with open(filename, 'r') as file:
        content = file.read().strip().split('\n')
        content = [re.split(r'\W+', item) for item in content]
        content = [[int(el[0]), int(el[1]), el[2], el[3]] for el in content]
        return content


def test_passwords_1(content):
    return [el for el in content 
            if int(el[0]) <= len(re.findall(el[2], el[3])) <= int(el[1])]


def test_passwords_2(content):
    def test(index, letter, pw):
        index -= 1
        return (pw[index] == letter) if (len(pw) >= index) else False
    
    return [el for el in content if test(el[0], *el[2:]) != test(*el[1:])]


if __name__ == '__main__':
    file_content = get_content('input')
    results = test_passwords_1(file_content)
    print(f'problem 1 - the solution is: {len(results)}')
    results = test_passwords_2(file_content)
    print(f'problem 2 - the solution is: {len(results)}')

