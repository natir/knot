#!/usr/bin/env python3

import sys
import argparse

from knot.extremity_search import *

def main(args):

    if args is None:
        args = sys.argv[1:]
    
    parser = argparse.ArgumentParser(prog="extremity_search")

    parser.add_argument("asm_graph", type=argparse.FileType('r'),
                        help="assembly graph")
    parser.add_argument("tig2tig", type=argparse.FileType('r'),
                        help="tig2tig graph")
    parser.add_argument("read2tig", type=argparse.FileType('r'),
                        help="read mapped against asm")
    parser.add_argument("read2read", type=argparse.FileType('r'),
                        help="SG graph")
    parser.add_argument("output", type=argparse.FileType('w'),
                        help="file where extremity are writed")
    
    args = parser.parse_args(args)
    args = vars(args)

    valid_read = get_valid_read(args["read2read"]) # read name

    tig2posread = get_tig2posread(args["read2tig"], valid_read) # tig -> (begin, end, name)
    for k in tig2posread:
        tig2posread[k].sort()

    ext_not_search = list(sum(get_ext_ovl(args["asm_graph"], args["tig2tig"]), ())) # tig1 -> tig2 tig1_end tig2_begin
    
    print("tig","read","strand_to_tig", sep=",", file=args["output"])

    for tig in tig2posread.keys():
        ext = tig+"_begin"
        if ext in ext_not_search:
            continue

        print(ext, tig2posread[tig][0][1], tig2posread[tig][0][2],
              sep=",", file=args["output"])
        
        ext = tig+"_end"
        if ext in ext_not_search:
            continue
        
        print(ext, tig2posread[tig][-1][1], tig2posread[tig][-1][2],
              sep=",", file=args["output"])


if __name__ == '__main__':
    main(sys.argv[1:])

