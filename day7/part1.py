#!/usr/bin/env python

import re
import math
import argparse
from copy import copy

class BeamDiagram:
    def __init__(self, lines):
        self.lines = [list(l) for l in lines]
        self.split_count = 0

    def __repr__(self):
        return "\n".join(self.get_lines())

    def get_lines(self):
        return ["".join(l) for l in self.lines]

    def beam_at(self, line_index, beam_index):
        self.lines[line_index][beam_index] = '|'

    def beamtime(self):
        beams = [self.lines[0].index('S')]
        for line_index,l in enumerate(self.lines):
            if not line_index:
                continue
            next_beams = []
            for i in beams:
                if l[i] == '.':
                    self.beam_at(line_index, i)
                    next_beams.append(i)
                elif l[i] == '^':
                    self.split_count += 1
                    next_beams.append(i-1)
                    next_beams.append(i+1)
                    self.beam_at(line_index, i-1)
                    self.beam_at(line_index, i+1)
            beams = next_beams

    def final_beam_count(self):
        return len([c for c in self.lines[-1] if c == '|'])

def parse_file(filename):
    lines = []
    with open(filename, "r") as fh:
        lines = [x.strip() for x in fh]
    return lines


def main(args):
    lines = parse_file(args.file)
    diag = BeamDiagram(lines)
    diag.beamtime()
    print(diag)
    print(diag.split_count)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='file', required=True)
    parser.add_argument('-d', '--debug', help='Debug', default=False, action="store_true")
    args = parser.parse_args()

    main(args)