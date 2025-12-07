#!/usr/bin/env python

import re
import math
import argparse
from copy import copy

DEBUG = False

class BeamNode:
    def __init__(self, line, index, entry_score=0):
        self.line = line
        self.index = index
        self.left = None
        self.right = None
        self.center = None
        self.parents = []
        self.entry_score = entry_score

    @property
    def id(self):
        return f"{self.line}:{self.index}"

    def add_parent(self, beamnode):
        self.parents.append(beamnode)
        self.entry_score += beamnode.entry_score

    def set_left(self, beamnode):
        if not beamnode:
            print("set_left called with None")
        self.left = beamnode
        beamnode.add_parent(self)

    def set_center(self, beamnode):
        if not beamnode:
            print("set_center called with None")
        self.center = beamnode
        beamnode.add_parent(self)

    def set_right(self, beamnode):
        if not beamnode:
            print("set_right called with None")
        self.right = beamnode
        beamnode.add_parent(self)

    def get_lineage(self, id, ids):
        if (self.id == id) or \
           (self.left_beam and self.left_beam.get_lineage(id, ids)) or \
           (self.right_beam and self.right_beam.get_lineage(id, ids)):
            ids[self.id] = True
            return True
        return False

class BeamDiagram:
    def __init__(self, lines):
        self.lines = [list(l) for l in lines]

    def __repr__(self):
        return "\n".join(self.get_lines())

    def highlight_routes(self, root_beam, id):
        diag = self.copy()
        lineage = {}
        root_beam.get_lineage(id, lineage)
        for i in lineage.keys():
            (line_index, col_index) = map(int, i.split(':'))
            diag.mark_beam(line_index, col_index, beam_char="x")
        print(diag)

    def copy(self):
        lines = self.get_lines()
        return BeamDiagram(copy(lines))

    @classmethod
    def get_line(cls, line):
        return "".join(line)

    def get_lines(self):
        return [BeamDiagram.get_line(l) for l in self.lines]

    def mark_beam(self, line_index, beam_index, beam_char='|'):
        self.lines[line_index][beam_index] = beam_char

    def beamtime(self):
        root = BeamNode(0, self.lines[0].index('S'), entry_score=1)
        beams = [root]
        for line_index,l in enumerate(self.lines):
            if not line_index:
                continue
            next_beams = []
            dprint(f"LINE: {BeamDiagram.get_line(l)}")
            for bi,b in enumerate(beams):
                i = b.index
                dprint(f"line {line_index}, {b.id} @ {i} ({l[i]})")
                if l[i] == '.':
                    dprint("continuing existing beam")
                    self.mark_beam(line_index, i)
                    next_beams.append(b)
                elif l[i] == '|':
                    pass
                    dprint("Existing beam '|' found, nothing to do")
                elif l[i] == '^':
                    self.mark_beam(line_index, i-1)
                    self.mark_beam(line_index, i+1)

                    # ----- LEFT BEAM -----

                    # Already a beam node to the left?
                    if next_beams and next_beams[-1].index == i-1:
                        existing_beam = next_beams[-1]

                        # Check if it came from above, so we'd need to add a new node
                        #   If we'd created a beam from a fork to the left, 
                        #   it'd have the same line index.
                        if existing_beam.line != line_index:
                            dprint("Existing beam to the left came from upstream only")
                            new_beam = BeamNode(line_index, i-1)
                            existing_beam.set_center(new_beam)
                            b.set_left(new_beam)
                            next_beams[-1] = new_beam
                        else:
                            dprint("Existing beam to the left can be reused")
                            b.set_left(existing_beam)
                    else:
                        new_beam = BeamNode(line_index, i-1)
                        dprint(f"new left beam, id = {new_beam.id}")
                        b.set_left(new_beam)
                        next_beams.append(new_beam)


                    # ----- RIGHT BEAM -----

                    # Already a beam node to the right, coming from above?
                    if len(beams) >= bi + 2 and beams[bi+1].index == i+1:
                        existing_beam = beams[bi+1]
                        dprint(f"existing right beam, id = {existing_beam.id}")
                        new_beam = BeamNode(line_index, i+1)
                        existing_beam.set_center(new_beam)
                        b.set_right(new_beam)
                        next_beams.append(new_beam)
                    else:
                        new_beam = BeamNode(line_index, i+1)
                        dprint(f"new right beam, id = {new_beam.id}")
                        b.set_right(new_beam)
                        next_beams.append(new_beam)
                else:
                    print(f"****** Unexpected char ({l[i]}) for beam id={b.id}")
            beams = next_beams
            next_beam_str = " ".join([b.id for b in beams])
            dprint(f"next beams: {next_beam_str}")
        return (root, beams)

    def final_beam_count(self):
        return len([c for c in self.lines[-1] if c == '|'])

def unique_beams(beam, beamkeys=None):
    if not beamkeys:
        beamkeys = {}

    traverse_beams(beam, beamkeys=beamkeys)
    return len(beamkeys)

def traverse_beams(beam, beamkeys, beampath=''):
    if beampath:
        beampath += '-'
    beampath += beam.id

    # Are we at the last node?
    if not beam.left_beam:
        # print(f"Last beam has beam path: {beampath}")
        beamkeys[beampath] = True
        return

    # print(f"Beam is splitting with beampath: {beampath}")
    traverse_beams(beam.left_beam, beamkeys=beamkeys, beampath=beampath)
    traverse_beams(beam.right_beam, beamkeys=beamkeys, beampath=beampath)


def parse_file(filename):
    lines = []
    with open(filename, "r") as fh:
        lines = [x.strip() for x in fh]
    return lines

def dprint(s):
    global DEBUG
    if DEBUG:
        print(s)

def main(args):
    global DEBUG
    if args.debug:
        DEBUG = True

    lines = parse_file(args.file)
    diag = BeamDiagram(lines)
    (root, final_beams) = diag.beamtime()
    print(diag)
    unique_paths = sum([b.entry_score for b in final_beams])
    print(f"Unique paths: {unique_paths}")
    # beamkeys = {}
    # total = unique_beams(root)
    # print(total)
    # diag.highlight_routes(root, '14:4')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='file', required=True)
    parser.add_argument('-d', '--debug', help='Debug', default=False, action="store_true")
    args = parser.parse_args()

    main(args)