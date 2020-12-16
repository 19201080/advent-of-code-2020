#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import re


def get_content(name):
    with open(name, 'r') as file:
        content = file.read().strip().split('\n\n')
        rules = [re.match(r'([\w\s]+): (\d+)-(\d+) or (\d+)-(\d+)', el).groups()
                 for el in content[0].split('\n')]
        rules = [[int(el) if el.isnumeric() else el for el in rule]
                 for rule in rules]
        your_ticket = [int(el) for el in content[1].split('\n')[1].split(',')]
        nearby_tickets = [[int(el) for el in ticket.split(',')]
                          for ticket in content[2].split('\n')[1:]]
        return rules, your_ticket, nearby_tickets


def apply_rules(field, rules):
    def apply_rule(ticket, rule):
        if rule[1] <= ticket <= rule[2] or rule[3] <= ticket <= rule[4]:
            return rule[0]
        return ticket
    return [apply_rule(field, rule) for rule in rules]


def get_invalid_field(field):
    if not any(el for el in field if isinstance(el, str)):
        return field[0]
    return None


def get_invalid_tickets(tickets, rules):
    res = [[get_invalid_field(apply_rules(field, rules)) for field in ticket]
           for ticket in tickets]
    return [{idx: field} for idx, ticket in enumerate(res)
            for field in ticket if field is not None]


def get_valid_tickets(tickets, invalid_tickets, rules):
    invalid_indexes = [key for ticket in invalid_tickets
                       for key in ticket.keys()]
    valid_tickets = [[apply_rules(field, rules) for field in ticket]
                     for idx, ticket in enumerate(tickets)
                     if idx not in invalid_indexes]
    return [[[rule for rule in field if isinstance(rule, str)]
             for field in ticket]
            for ticket in valid_tickets]


def get_fields_rules(tickets):
    fields = defaultdict(list)
    for ticket_idx, ticket in enumerate(tickets):
        for field_idx, field in enumerate(ticket):
            fields[field_idx].append(set(field))
    fields = {k: set.intersection(*v) for k, v in fields.items()}
    while any(len(value) > 1 for value in fields.values()):
        for k, v in fields.items():
            if len(v) < 2:
                fields = {key: (value - v if key != k else value)
                          for key, value in fields.items()}
    return {k: list(v)[0] for k, v in fields.items()}


def your_ticket_departure(ticket, field_rules):
    fields = [k for k, v in field_rules.items() if v.startswith('departure')]
    result = 1
    for idx, value in enumerate(ticket):
        if idx in fields:
            result *= value
    return result


def run():
    rules, your_ticket, nearby_tickets = get_content('input')
    invalid_tickets = get_invalid_tickets(nearby_tickets, rules)
    result = sum(val for ticket in invalid_tickets for val in ticket.values())
    print(f'problem 1 - the solution is: {result}')
    valid_tickets = get_valid_tickets(nearby_tickets, invalid_tickets, rules)
    fields = get_fields_rules(valid_tickets)
    result = your_ticket_departure(your_ticket, fields)
    print(f'problem 2 - the solution is: {result}')


if __name__ == '__main__':
    run()
