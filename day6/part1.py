#!/usr/bin/env python

import re
import math
import argparse
from copy import copy

class Problem:
    def __init__(self):
        self.numbers = []
        self.operator = None

    def __repr__(self):
        return self.operator.join(map(str, self.numbers))

    def add_number(self, n):
        self.numbers.append(int(n))

    def add_operator(self, o):
        self.operator = o

    def run(self):
        if self.operator == '+':
            return sum(self.numbers)

        if self.operator == '*':
            return math.prod(self.numbers)

        return "unsupported"

def parse_file(filename):
    lines = []
    with open(filename, "r") as fh:
        for line in fh:
            line = line.strip()
            lines.append(re.split(r'\s+', line))
    return lines


def main(args):
    math_lines = parse_file(args.file)

    problems = [Problem() for i in range(len(math_lines[0]))]
    for l in math_lines:
        for i,x in enumerate(l):
            if x.isdigit():
                problems[i].add_number(x)
            else:
                problems[i].add_operator(x)

    total = 0
    for p in problems:
        total += p.run()

    print(f"total: {total}")




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='file', required=True)
    parser.add_argument('-d', '--debug', help='Debug', default=False, action="store_true")
    args = parser.parse_args()

    main(args)