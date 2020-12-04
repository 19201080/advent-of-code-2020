#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

byr = 'byr'
iyr = 'iyr'
eyr = 'eyr'
hgt = 'hgt'
hcl = 'hcl'
ecl = 'ecl'
pid = 'pid'
cid = 'cid'

passport_keys = [byr, iyr, eyr, hgt, hcl, ecl, pid, cid]


def get_content(name):
    with open(name, 'r') as file:
        content = file.read().strip().split('\n\n')
        content = [re.split(r'\s|\n', el) for el in content]

        def passport_to_dict(passport):
            result = {}
            for el in passport:
                el = el.split(':')
                result[el[0]] = el[1]
            return result

        return [passport_to_dict(passport) for passport in content]


def get_valid_formats(content, *missing_keys):
    valid_length = len(passport_keys) - len(missing_keys)
    return [passport for passport in content
            if len(passport) == valid_length
            and all(key not in passport for key in missing_keys)]


def get_valid_values(content):
    def check_values(passport):
        check_byr = 1920 <= int(passport[byr]) <= 2002
        check_iyr = 2010 <= int(passport[iyr]) <= 2020
        check_eyr = 2020 <= int(passport[eyr]) <= 2030
        if hgt_v := re.match(r'(\d+)(\w+)', passport[hgt]):
            check_hgt = (hgt_v[2] == 'cm' and 150 <= int(hgt_v[1]) <= 193) \
                        or (hgt_v[2] == 'in' and 59 <= int(hgt_v[1]) <= 76)
        else:
            check_hgt = False
        check_hcl = bool(re.match(r'#(\d|[a-f]){6}$', passport[hcl]))
        check_ecl = passport[ecl] in ('amb', 'blu', 'brn', 'gry',
                                      'grn', 'hzl', 'oth')
        check_pid = bool(re.match(r'\d{9}$', passport[pid]))
        return all((check_byr, check_iyr, check_eyr, check_hgt,
                    check_hcl, check_ecl, check_pid))

    return [passport for passport in content if check_values(passport)]


if __name__ == '__main__':
    file_content = get_content('input')
    full_passports = get_valid_formats(file_content)
    passports_without_cid = get_valid_formats(file_content, cid)
    result = len(full_passports + passports_without_cid)
    print(f'problem 1 - the solution is {result}')

    valid_passports = get_valid_values(full_passports + passports_without_cid)
    result = len(valid_passports)
    print(f'problem 2 - the solution is {result}')
