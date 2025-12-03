#!/usr/bin/env python

import re
import argparse

class Dial:
    def __init__(self, starting_value, min_number=0, max_number=99):
        self.min_number = min_number
        self.max_number = max_number + 1 # adjust for 0
        self.value = starting_value

    def turn(self, direction, clicks):
        if direction == "L":
            clicks *= -1
        self.value += clicks

        while self.value < 0:
            self.value = self.max_number + self.value

        self.value = self.value % self.max_number

def parse_file(filename):
    commands = []
    with open(filename, "r") as fh:
        for line in fh:
            if not line.strip():
                continue
            mobj = re.match(r'(L|R)(\d+)', line)
            if mobj:
                commands.append((mobj.group(1), int(mobj.group(2))))
    return commands

def main(args):
    dial = Dial(starting_value=50)
    commands = parse_file(args.file)
    zero_count = 0
    for (direction, clicks) in commands:
        dial.turn(direction, clicks)
        print(f"The dial is at {dial.value}")
        if dial.value == 0:
            zero_count += 1

    print(f"zero count: {zero_count}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='file', required=True)
    args = parser.parse_args()

    main(args)