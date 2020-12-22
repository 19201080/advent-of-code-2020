#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_input(filename):
    with open(filename, 'r') as f:
        decks = f.read().split('\n\n')
        return [[int(number) for number in deck.split('\n')[1:]]
                for deck in decks]


def do_a_round(deck1, deck2):
    card1 = deck1.pop(0)
    card2 = deck2.pop(0)
    (deck2 if card2 > card1 else deck1).extend(sorted((card1, card2))[::-1])
    return deck1, deck2


def do_rounds(input1, input2):
    deck1 = input1[:]
    deck2 = input2[:]
    while deck1 and deck2:
        deck1, deck2 = do_a_round(deck1, deck2)
    return deck1 or deck2


def do_a_recursive_round(deck1, deck2, memo=None):
    memo = memo or []
    memo.extend((deck1[:], deck2[:]))
    if len(deck1) == 0 or len(deck2) == 0:
        return deck1, deck2, memo

    card1 = deck1.pop(0)
    card2 = deck2.pop(0)

    if len(deck1) >= card1 and len(deck2) >= card2:
        result = do_recursive_game(deck1[:][:card1], deck2[:][:card2])
        cards = (card1, card2) if result[0] else (card2, card1)
        (deck1 if result[0] else deck2).extend(cards)
    else:
        (deck1 if card1 > card2 else deck2).extend(sorted((card1, card2))[::-1])
    return deck1, deck2, memo


def do_recursive_game(input1, input2):
    deck1 = input1[:]
    deck2 = input2[:]
    memo = []
    while deck1 and deck2:
        if (deck1 in memo) or (deck2 in memo):
            return deck1, [], []
        deck1, deck2, memo = do_a_recursive_round(deck1, deck2, memo)
    return deck1, deck2


def compute_score(deck):
    return sum([card * (idx + 1) for idx, card in enumerate(deck[::-1])])


def main():
    file_content = get_input('input')
    winning_deck = do_rounds(*file_content)
    result = compute_score(winning_deck)
    print(f'problem 1 - the result is: {result}')

    deck1, deck2 = do_recursive_game(*file_content)
    result = compute_score(deck1 or deck2)
    print(f'problem 2 - the result is: {result}')


if __name__ == '__main__':
    main()
