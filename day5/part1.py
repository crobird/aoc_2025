#!/usr/bin/env python

import re
import argparse
from copy import copy

# Wrong: 979

class Produce():
    def __init__(self):
        self.fresh_ranges = []
        self.ids = []

    @classmethod
    def range_string(cls, range):
        return f"{range[0]} - {range[1]}"

    def __repr__(self):
        return "\n".join([Produce.range_string(r) for r in self.fresh_ranges])

    def add_range(self, r):
        self.fresh_ranges.append(r)

    def add_id(self, product_id):
        self.ids.append(product_id)

    def is_fresh(self, product_id):
        for r in self.fresh_ranges:
            print(f"Checking if {product_id} > {r[0]} and > {r[1]}")
            if product_id > r[0] and product_id < r[1]:
                return True
        return False

def parse_file(filename, produce):
    lines = None
    with open(filename, "r") as fh:
        for line in fh:
            line = line.strip()
            mobj = re.match(r'(\d+)\-(\d+)$', line)
            if mobj:
                produce.add_range((int(mobj.group(1)), int(mobj.group(2))))
                continue

            mobj = re.match(r'(\d+)$', line)
            if mobj:
                produce.add_id(int(mobj.group(1)))
                continue

    return lines


def main(args):
    produce = Produce()
    parse_file(args.file, produce)
    fresh_count = 0
    for i in produce.ids:
        print(f"checking id {i}")
        if produce.is_fresh(i):
            fresh_count += 1

    print(f"Fresh items: {fresh_count}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='file', required=True)
    parser.add_argument('-d', '--debug', help='Debug', default=False, action="store_true")
    args = parser.parse_args()

    main(args)