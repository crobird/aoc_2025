#!/usr/bin/env python

import re
import math
import argparse
from copy import copy

class Problem:
    def __init__(self):
        self.numbers = []
        self.ceph_numbers = []
        self.operator = None

    def __repr__(self):
        return "human:" + self.operator.join(self.numbers) + "\nceph: " + self.operator.join(map(str, self.ceph_numbers))

    def add_human_number(self, n):
        self.numbers.append(n)

    def add_operator(self, o):
        self.operator = o

    def compute_ceph_numbers(self):
        max_len = max(map(len, self.numbers))
        for nindex in reversed(range(max_len)):
            new_num = ''
            for n in self.numbers:
                if n[nindex].isdigit():
                    new_num += n[nindex]
            self.ceph_numbers.append(int(new_num)) 

    def run(self):
        if self.operator == '+':
            return sum(self.ceph_numbers)

        if self.operator == '*':
            return math.prod(self.ceph_numbers)

        return "unsupported"

def parse_file(filename):
    lines = []
    with open(filename, "r") as fh:
        lines = [x.strip("\n") for x in fh]


    operator_indexes = []
    for i,c in enumerate(lines[-1]):
        if c != ' ':
            operator_indexes.append(i)

    print("\n".join(lines))
    number_lines = []
    for l in lines:
        number_strs = []
        for i,oi in enumerate(operator_indexes):
            if i == 0:
                continue

            start = operator_indexes[i-1]
            end = oi-1
            new_num = l[start:end]
            number_strs.append(new_num)

        # Don't forget the last one, since we appended starting on the second element
        number_strs.append(l[end+1:])
        number_lines.append(number_strs)

    return number_lines


def main(args):
    math_lines = parse_file(args.file)

    problems = [Problem() for i in range(len(math_lines[0]))]
    for l in math_lines:
        for i,x in enumerate(l):
            if x.strip().isdigit():
                problems[i].add_human_number(x)
            else:
                problems[i].add_operator(x.strip())

    total = 0
    for p in problems:
        p.compute_ceph_numbers()
        total += p.run()

    print(f"total: {total}")




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='file', required=True)
    parser.add_argument('-d', '--debug', help='Debug', default=False, action="store_true")
    args = parser.parse_args()

    main(args)