#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import re

import numpy as np

SEA_MONSTER = ['                  # ',
               '#    ##    ##    ###',
               ' #  #  #  #  #  #   ']
SEA_MONSTER_SYMBOLS = [
    (line_idx - 1, char_idx) for line_idx, line in enumerate(SEA_MONSTER)
    for char_idx, char in enumerate(line) if char == '#']
EMPTY_BLOCK = 'empty'


def get_content(filename):
    with open(filename, 'r') as f:
        content = [block.split('\n') for block in f.read().split('\n\n')]
        return {int(re.search(r'(\d+)', block[0])[0]): block[1:]
                for block in content}


def find_border_occurrences(content):
    unique_borders = defaultdict(int)
    for block in content:
        for side in block.borders_options:
            for border in side:
                unique_borders[border] += 1
    unique_borders = [k for k, v in unique_borders.items() if v < 2]

    for block in content:
        block.shared_borders = [[border for border in side
                                 if border not in unique_borders]
                                for side in block.borders_options]
    return content


class Block:
    def __init__(self, idx, content):
        self.idx = idx
        self.content = np.array(content)
        self._shared_borders = None
        self.is_corner = False
        self.flipped_ud = False
        self.flipped_lr = False
        self.surrounded = False

    @property
    def borders(self):
        return self.get_borders()

    @property
    def borders_options(self):
        return [[side, side[::-1]] for side in self.get_borders()]

    @property
    def shared_borders(self):
        return [[self.borders[idx]] if side else []
                for idx, side in self._shared_borders]

    @shared_borders.setter
    def shared_borders(self, content):
        self._shared_borders = [(idx, bool(side))
                                for idx, side in enumerate(content)]
        if len([side for side in content if side]) == 2:
            self.is_corner = True
        else:
            self.is_corner = False

    def __repr__(self):
        return str(self.idx)

    def rotate(self, angle):
        split_content = np.array([list(line) for line in self.content])
        rotated_content = np.rot90(split_content, angle)
        self.content = np.array([''.join(line) for line in rotated_content])
        self._shared_borders = sorted(
            [((idx + angle) % 4, side)
             for idx, side in self._shared_borders], key=lambda x: x[0])

    def flip_ud(self):
        split_content = np.array([list(line) for line in self.content])
        flipped_content = np.flipud(split_content)
        self.content = np.array([''.join(line) for line in flipped_content])
        self._shared_borders = sorted([
            ((idx + 2) % 4, side) if idx in (0, 2) else (idx, side)
            for idx, side in self._shared_borders], key=lambda x: x[0])
        self.flipped_ud = not self.flipped_ud

    def flip_lr(self):
        split_content = np.array([list(line) for line in self.content])
        flipped_content = np.fliplr(split_content)
        self.content = np.array([''.join(line) for line in flipped_content])
        self._shared_borders = sorted([
            ((idx + 2) % 4, side) if idx in (1, 3) else (idx, side)
            for idx, side in self._shared_borders], key=lambda x: x[0])
        self.flipped_lr = not self.flipped_lr

    def flip_both(self):
        self.flip_lr()
        self.flip_ud()

    def flip(self):
        options = {
            (False, False): lambda: self.flip_lr(),
            (False, True): lambda: self.flip_both(),
            (True, False): lambda: self.flip_lr(),
            (True, True): lambda: self.flip_both()}
        options[(self.flipped_ud, self.flipped_lr)]()

    def get_borders(self):
        top = self.content[0]
        bottom = self.content[-1]
        left = ''.join([line[0] for line in self.content])
        right = ''.join([line[-1] for line in self.content])
        return [top, left, bottom, right]

    def all_other_borders(self, content):
        return {block: block.borders for block in content
                if block is not self}

    def get_shared_borders(self, content):
        all_other_borders = self.all_other_borders(content)
        shared_borders = {idx: [(k, other_idx)
                                for k, v in all_other_borders.items()
                                for other_idx, other_side in enumerate(v)
                                if side == other_side]
                          for idx, side in enumerate(self.borders)}

        self.shared_borders = shared_borders
        return content


def add_empty_neighbors(array, block):
    for side_idx, side in enumerate(block.shared_borders):
        block_y, block_x = np.array(*zip(*np.where(array == block)))
        if not any(el for el in side):
            continue
        if side_idx in (0, 2):
            if block_y + side_idx - 1 not in range(len(array)):
                array = np.insert(array, max(0, block_y + side_idx - 1),
                                  EMPTY_BLOCK, axis=0)
        if side_idx in (1, 3):
            if block_x + side_idx - 2 not in range(len(array[block_y])):
                array = np.insert(array, max(0, block_x + side_idx - 2),
                                  EMPTY_BLOCK, axis=1)
    return array


def get_common_borders(block_loc, neighbor_loc, results):
    rel_x, rel_y = np.array(neighbor_loc) - np.array(block_loc)
    border_idx = abs(rel_x) * (rel_x + 1) + abs(rel_y) * (rel_y + 2)
    return border_idx, results[block_loc[0]][block_loc[1]].borders[border_idx]


def build_image(content):
    first_corner = [block for block in content if block.is_corner][0]
    results = np.array([[first_corner]])
    results = add_empty_neighbors(results, first_corner)

    while EMPTY_BLOCK in results:
        block = [block for block in results.flatten()
                 if block != EMPTY_BLOCK and not block.surrounded][0]
        block_location = list(zip(*np.where(results == block)))[0]
        directions = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1)
                      if (x or y) and (not x or not y)]
        neighbors_locations = [(block_location[0] + x, block_location[1] + y)
                               for x, y in directions]
        neighbors_locations = [neighbor for neighbor in neighbors_locations
                               if neighbor[0] in range(len(results))
                               and neighbor[1] in range(len(results[0]))]
        empty_neighbors = [location for location in neighbors_locations
                           if results[location[0]][location[1]] == EMPTY_BLOCK]

        if not empty_neighbors:
            block.surrounded = True
            continue

        open_borders = [(neighbor_loc, *get_common_borders(block_location,
                                                           neighbor_loc,
                                                           results))
                        for neighbor_loc in empty_neighbors]

        for location, border_idx, border in open_borders[:1]:
            match_block = [(block, idx, side) for block in content
                           for idx, side in enumerate(block.borders_options)
                           if border in side
                           and block not in results.flatten()]

            match_block = match_block[0]

            match_idx = (match_block[1] + 2) % 4
            if border_idx != match_idx:
                angle = border_idx - match_idx
                match_block[0].rotate(angle)
                for idx, side in enumerate(match_block[0].borders_options):
                    if border in side:
                        match_block = (match_block[0], idx, side)

            if border == match_block[2][1]:
                if match_block[1] in (1, 3):
                    match_block[0].flip_ud()
                else:
                    match_block[0].flip_lr()
                for idx, side in enumerate(match_block[0].borders_options):
                    if border in side:
                        match_block = (match_block[0], idx, side)

            results[location[0]][location[1]] = match_block[0]
            results = add_empty_neighbors(results, match_block[0])
    return results


def list_mul(content):
    result = 1
    for item in content:
        result *= item
    return result


def stitch_image(image):
    new_image = []
    block_size = len(image[0][0].content) - 2
    for line_idx, line in enumerate(image):
        new_image.extend([] for _ in range(block_size))
        for block in line:
            for el_idx, element in enumerate(block.content[1:-1]):
                new_image[block_size * line_idx + el_idx].append(element[1:-1])
    return np.array([''.join(line) for line in new_image])


def split_image(image):
    return np.array([list(line) for line in image])


def join_image(image):
    return [''.join(line) for line in image]


def search_sea_monster(image):
    found_sea_monsters = []
    for flipped in (True, False):
        for orientation in range(4):
            changed_image = image[:]
            if flipped:
                changed_image = np.flipud(changed_image)
            changed_image = np.rot90(changed_image, orientation)
            cropped_image = changed_image[:-len(SEA_MONSTER) + 2,
                                          :-len(SEA_MONSTER[0]) + 1]
            image_symbols = [(line_idx, char_idx)
                             for line_idx, line in enumerate(cropped_image)
                             for char_idx, char in enumerate(line)
                             if char == '#']
            valid_monsters = [symbol for symbol in image_symbols
                              if all(changed_image
                                     [monster[0] + symbol[0]]
                                     [monster[1] + symbol[1]] == '#'
                                     for monster in SEA_MONSTER_SYMBOLS)]
            found_sea_monsters.append(((flipped, orientation), valid_monsters))
    found_sea_monsters = [(config, amount)
                          for config, amount in found_sea_monsters if amount]
    return found_sea_monsters


def highlight_sea_monsters(image, config, monsters_tails):
    flipped, orientation = config
    new_image = image
    if flipped:
        new_image = np.flipud(new_image)
    new_image = np.rot90(new_image, orientation)
    for tail in monsters_tails:
        for symbol in SEA_MONSTER_SYMBOLS:
            new_image[tail[0] + symbol[0]][tail[1] + symbol[1]] = 'O'
    return new_image


def main():
    file_content = get_content('input')
    file_content = np.array([Block(k, v) for k, v in file_content.items()])
    find_border_occurrences(file_content)
    corners = [block for block in file_content if block.is_corner]
    result = list_mul([corner.idx for corner in corners])
    print(f'problem 1 - the solution is: {result}')

    splitted_image = split_image(stitch_image(build_image(file_content)))
    config, tails = search_sea_monster(splitted_image)[0]
    with_monsters = highlight_sea_monsters(splitted_image, config, tails)

    result = sum(element == '#' for element in with_monsters.flatten())
    print(f'problem 2 - the solution is: {result}')

    print('\nimage:')
    for line in join_image(with_monsters):
        print(line)


if __name__ == '__main__':
    main()
