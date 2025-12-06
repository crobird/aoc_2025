#!/usr/bin/env python

import re
import argparse
from copy import copy
from itertools import groupby

#1 Too low:   30666345750939
#2 Too high: 515280445427025
#3 Too low:  343020009886236
#4           277867905612946
#5           373020168988732
#6           351038459100184
#finally     357907198933892

class Produce():
    def __init__(self):
        self.ranges = []
        self.ids = []

    def range_string(self, rng):
        return f"{rng[0]} - {rng[1]}"

    def __repr__(self):
        return "--\n" + "\n".join([self.range_string(r) for r in self.ranges]) + f"\nrange count: {len(self.ranges)}"

    def add_range(self, new_range):
        self.ranges.append(new_range)

    def collapse_ranges(self):
        new_ranges = [[] for r in self.ranges]
        made_mods = False
        for i,r in enumerate(self.ranges):
            new_ranges[i].extend(r)
            for ic,comp in enumerate(self.ranges):
                if ic == i:
                    continue
                new_ranges[ic].extend(comp)
                if Produce.has_overlap(r, comp) and r != comp:
                    made_mods = True
                    new_ranges[i].extend(comp)
                    new_ranges[ic].extend(r)

        new_ranges = [[min(x), max(x)] for x in new_ranges]

        # Clear out duplicates
        self.ranges = []
        for r in new_ranges:
            if r not in self.ranges:
                self.ranges.append(r)

        if made_mods:
            self.collapse_ranges()


    def add_range2(self, new_range):
        print(f"Adding new range {new_range}")
        added_index = None
        for i,r in enumerate(self.ranges):
            if Produce.in_range(r, new_range[0]):
                added_index = i
                r.append(new_range[1])
            elif Produce.in_range(r, new_range[1]):
                added_index = i
                r.append(new_range[0])

        if not added_index:
            added_index = len(self.ranges)
            self.ranges.append(new_range)

        min_value = self.ranges[added_index][0]
        max_value = max(self.ranges[added_index])
        self.ranges[added_index] = [min_value, max_value]

        new_end_value = None
        for i,r in enumerate(self.ranges):
            if i == added_index:
                continue
            if Produce.in_range(self.ranges[added_index], r[0]):
                new_end_value = r[1]
                break

        if new_end_value:
            self.ranges[added_index][1] = new_end_value
            del self.ranges[i]

    @classmethod
    def has_overlap(cls, r1, r2):
        return Produce.in_range(r1, r2[0]) or Produce.in_range(r1, r2[1])        

    @classmethod
    def in_range(cls, r, n):
        if n >= r[0] and n <= r[1]:
            return True
        return False

    @property
    def range_keys(self):
        return self.ranges.keys()

    # def collapse_ranges(self):
    #     change_made = False

    #     new_ranges = {}
    #     for rng in self.range_keys:
    #         # print(f"+ rng = {rng} ")
    #         if not self.ranges[rng]:
    #             # print(f"skipping rng {rng}")
    #             continue
    #         for comp in self.range_keys:
    #             # print(f"+ comp = {comp} ")
    #             if not self.ranges[comp]:
    #                 # print(f"skipping comp {comp}")
    #                 continue
    #             if rng == comp:
    #                 if rng not in new_ranges:
    #                     # print(f"Adding self to new_ranges {rng}")
    #                     new_ranges[rng] = self.ranges[rng]
    #                 continue
                    
    #             start_inside = True if Produce.in_range(comp, rng[0]) else False
    #             end_inside   = True if Produce.in_range(comp, rng[1]) else False

    #             if not start_inside and not end_inside:
    #                 continue

    #             if start_inside and end_inside:
    #                 # print(f"Setting to false cause inside {rng}, {comp}")
    #                 new_ranges[rng] = False
    #                 break

    #             if start_inside:
    #                 new_range = (comp[0], rng[1])
    #             elif end_inside:
    #                 new_range = (rng[0], comp[1])

    #             if new_range not in new_ranges:
    #                 # print(f"Setting to false cause new range {rng} -> {new_range}")
    #                 change_made = True
    #                 new_ranges[new_range] = True
    #                 new_ranges[rng] = False
    #                 new_ranges[comp] = False

    #         # print(new_ranges)

    #     if change_made:
    #         self.ranges = new_ranges
    #         # print("--------------------------")
    #         self.collapse_ranges()

    def fresh_product_count(self):
        fresh_count = 0
        for r in self.ranges:
            fresh_count += (r[1] - r[0]) + 1
        return fresh_count

def parse_file(filename, produce):
    lines = None
    with open(filename, "r") as fh:
        for line in fh:
            line = line.strip()
            mobj = re.match(r'(\d+)\-(\d+)$', line)
            if mobj:
                produce.add_range([int(mobj.group(1)), int(mobj.group(2))])
                continue

    return lines


def main(args):
    produce = Produce()
    parse_file(args.file, produce)
    print(produce)
    produce.collapse_ranges()
    print(produce)

    count = produce.fresh_product_count()
    print(f"Fresh items: {count}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='file', required=True)
    parser.add_argument('-d', '--debug', help='Debug', default=False, action="store_true")
    args = parser.parse_args()

    main(args)