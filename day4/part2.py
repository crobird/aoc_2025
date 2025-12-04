#!/usr/bin/env python

import re
import argparse
from copy import copy

class PaperPile:
    def __init__(self, paper_lines):
        self.rows = [list(x) for x in paper_lines]
        self.row_len = len(paper_lines[0])

    def __repr__(self):
        return "\n".join([''.join(r) for r in self.rows])

    def is_roll(self, y, x):
        if self.rows[y][x] == '.':
            return False
        return True

    def get_forkable_rolls(self, max_neighbors=3):
        forkable_rolls = []

        for y in range(len(self.rows)):
            for x in range(self.row_len):
                if not self.is_roll(y,x):
                    continue

                neighbor_rolls  = 0
                can_check_up    = True if y > 0 else False
                can_check_down  = True if y < len(self.rows) - 1 else False
                can_check_left  = True if x > 0 else False
                can_check_right = True if x < self.row_len - 1 else False

                if can_check_up:
                    if self.is_roll(y-1, x):
                        neighbor_rolls += 1

                    if can_check_left and self.is_roll(y-1, x-1):
                        neighbor_rolls += 1

                    if can_check_right and self.is_roll(y-1, x+1):
                        neighbor_rolls += 1

                if can_check_down:
                    if self.is_roll(y+1, x):
                        neighbor_rolls += 1

                    if can_check_left and self.is_roll(y+1, x-1):
                        neighbor_rolls += 1

                    if can_check_right and self.is_roll(y+1, x+1):
                        neighbor_rolls += 1

                if can_check_left and self.is_roll(y, x-1):
                    neighbor_rolls += 1

                if can_check_right and self.is_roll(y, x+1):
                    neighbor_rolls += 1

                if neighbor_rolls <= max_neighbors:
                    self.rows[y][x] = str(neighbor_rolls)
                    forkable_rolls.append((y,x))

        return forkable_rolls

    def remove_all_forkable_rolls(self, max_neighbors=3):
        keep_going = True
        forked_rolls = 0
        while keep_going:
            forkable_rolls = self.get_forkable_rolls(max_neighbors)
            if forkable_rolls:
                forked_rolls += len(forkable_rolls)
                for y,x in forkable_rolls:
                    self.rows[y][x] = '.'
            else:
                keep_going = False
        return forked_rolls


def parse_file(filename):
    lines = None
    with open(filename, "r") as fh:
        lines = [l.strip() for l in fh]
    return lines


def main(args):
    paper_lines = parse_file(args.file)
    paper_pile = PaperPile(paper_lines)
    forked_roll_count = paper_pile.remove_all_forkable_rolls()
    print(paper_pile)
    print(f"Forked rolls: {forked_roll_count}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='file', required=True)
    parser.add_argument('-d', '--debug', help='Debug', default=False, action="store_true")
    args = parser.parse_args()

    main(args)