#!/usr/bin/env python

# 6606 is too low
# 6521 is too low
# 7087 is too high

import re
import argparse

class Dial:
    def __init__(self, starting_value, min_number=0, max_number=99):
        self.min_number = min_number
        self.max_number = max_number + 1 # adjust for 0
        self.value = starting_value

    def turn(self, direction, clicks):
        clockwise = True if direction == "R" else False
        if not clockwise:
            clicks *= -1

        # Don't double count getting to zero
        zero_count = -1 if (self.value == 0 and not clockwise) else 0

        self.value += clicks

        if self.value == 0:
            return 1

        while self.value < self.min_number:
            zero_count += 1
            self.value = self.max_number + self.value

        if self.value == 0:
            zero_count += 1

        while self.value >= self.max_number:
            zero_count += 1
            self.value -= self.max_number

        return zero_count

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
        new_zero_count = dial.turn(direction, clicks)
        zero_count += new_zero_count
        print(f"{direction}{clicks} > {dial.value} (+{new_zero_count})")

    print(f"final zero count: {zero_count}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='file', required=True)
    args = parser.parse_args()

    main(args)