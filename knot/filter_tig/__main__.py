#!/usr/bin/env python3

import sys
import argparse

from Bio import SeqIO

def main(args):

    if args is None:
        args = sys.argv[1:]
    
    parser = argparse.ArgumentParser(prog="filter_contig")

    parser.add_argument("-t", "--threshold", default=100.000, type=int,
                        help="Only sequence with size upper than threshold are write in output default 100.000")
    parser.add_argument("input", type=argparse.FileType('r'), help="input fasta")
    parser.add_argument("output", type=argparse.FileType('w'), help="output fasta")
    
    args = parser.parse_args(args)
    args = vars(args)

    for record in SeqIO.parse(args["input"], "fasta"):
        if len(record.seq) > args["threshold"]:
            SeqIO.write(record, args["output"], "fasta")

if __name__ == '__main__':
    main(sys.argv[1:])
