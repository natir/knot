#!/usr/bin/env python3

# std import
import sys
import argparse

# pip import
from Bio import SeqIO

# project import
from knot import extremity_search

def main(args=None):

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(prog="knot.sg_generation")

    parser.add_argument("reads2contig", type=argparse.FileType('r'))
    parser.add_argument("input", type=argparse.FileType('r'))
    parser.add_argument("output", type=argparse.FileType('w'))

    args = vars(parser.parse_args(args))

    tig2readspos = extremity_search.get_tig2posread(args["reads2contig"], set())
    
    skip_read = set()
    for tig, val in tig2readspos.items():
        t = max(tig[1]*0.2, 100000)
        for v in val:
            if v[0] > t and v[1] < tig[1] - t:
                skip_read.add(v[2])

    for record in SeqIO.parse(args["input"], "fasta"):
        if record.id not in skip_read:
            SeqIO.write(record, args["output"], "fasta")

    
if __name__ == "__main__":
    main()
