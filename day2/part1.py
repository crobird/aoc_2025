#!/usr/bin/env python

import re
import argparse

def parse_file(filename):
    with open(filename, "r") as fh:
        for line in fh:
            if not line.strip():
                continue
            range_chunks = line.strip().split(',')
            return [c.split('-') for c in range_chunks]

def is_illegal(product_number):
    product = str(product_number)
    if len(product) % 2 != 0:
        return False
    half_len = int(len(product) / 2)
    left = product[:half_len]
    right = product[half_len:]
    if left == right:
        return True
    return False


def main(args):
    illegal_products = []
    ranges = parse_file(args.file)
    for (lnum, rnum) in ranges:
        if args.debug:
            print(f"{lnum}-{rnum}")
        for i in range(int(lnum), int(rnum) + 1):
            if is_illegal(i):
                illegal_products.append(i)
            if args.debug:
                print(f"{i}")
    
    sum_of_invalid_ids = sum(illegal_products)
    print(f"sum of invalid product ids: {sum_of_invalid_ids}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='file', required=True)
    parser.add_argument('-d', '--debug', help='Debug', default=False, action="store_true")
    args = parser.parse_args()

    main(args)