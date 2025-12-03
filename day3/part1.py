#!/usr/bin/env python

import re
import argparse
from copy import copy

class Bank:
    def __init__(self, joltage_string):
        self.joltages = list(joltage_string)

    def __repr__(self):
        return "".join(self.joltages)

    def find_max_joltages(self, battery_count):
        return Bank.max_joltages(self.joltages, battery_count)

    @classmethod
    def max_joltages(cls, remaining_joltages, battery_count, result=None):
        if not result:
            result = [] 
        joltages = list(enumerate(remaining_joltages))
        joltages.sort(key=lambda x: x[1], reverse=True)
        for i,j in joltages:
            if i + battery_count > len(remaining_joltages):
                # Not enough batteries after the max, so we need to move to the next possible max
                continue
            break
        result.append(j)
        if battery_count == 1:
            return result
        return Bank.max_joltages(remaining_joltages[i+1:], battery_count - 1, result)

def parse_file(filename):
    banks = []
    with open(filename, "r") as fh:
        for line in fh:
            if not line.strip():
                continue
            banks.append(Bank(line.strip()))
    return banks


def main(args):
    banks = parse_file(args.file)
    total = 0
    for bank in banks:
        print(bank)
        joltages = bank.find_max_joltages(args.battery_num)
        print(joltages)
        total += int(''.join(joltages))
    print(f"total: {total}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='file', required=True)
    parser.add_argument('-n', '--battery_num', help="Number of batteries for each bank", type=int, required=True)
    parser.add_argument('-d', '--debug', help='Debug', default=False, action="store_true")
    args = parser.parse_args()

    main(args)