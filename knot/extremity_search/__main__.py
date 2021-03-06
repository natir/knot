#!/usr/bin/env python3

import sys
import argparse

from knot.extremity_search import *

def main(args=None):

    if args is None:
        args = sys.argv[1:]
    
    parser = argparse.ArgumentParser(prog="knot.extremity_search")

    parser.add_argument("read2tig", type=argparse.FileType('r'),
                        help="read mapped against asm")
    parser.add_argument("read2read", type=argparse.FileType('r'),
                        help="SG graph")
    parser.add_argument("output", type=argparse.FileType('w'),
                        help="file where extremity are writed")
    
    args = parser.parse_args(args)
    args = vars(args)

    valid_read = get_valid_read(args["read2read"]) # read name
    
    # (tig, tig_len) -> (tig_begin, tig_end, name, read_begin, read_dist_to_end, read_ori)
    tig2posread = get_tig2posread(args["read2tig"], valid_read) 
    for k in tig2posread:
        tig2posread[k].sort()

    print("tig","read","strand_to_tig","dist2ext", sep=",", file=args["output"])

    for tig in tig2posread.keys():
        ext = tig[0]+"_begin"
        
        if tig2posread[tig][1][5] == "+":
            print(ext,
                  tig2posread[tig][1][2],
                  tig2posread[tig][1][5],
                  (tig2posread[tig][1][0] - tig2posread[tig][1][3]) * -1,
                  sep=",", file=args["output"])
        else:
            print(ext,
                  tig2posread[tig][1][2],
                  tig2posread[tig][1][5],
                  (tig2posread[tig][1][0] - tig2posread[tig][1][4]) * -1,
                  sep=",", file=args["output"])
            
        ext = tig[0]+"_end"
        tig2posread[tig].sort(key=lambda x: x[1])

        if tig2posread[tig][-2][5] == "+":
            print(ext,
                  tig2posread[tig][-2][2],
                  tig2posread[tig][-2][5],
                  ((tig[1] - tig2posread[tig][-2][1]) - tig2posread[tig][-2][4]) * -1,
                  sep=",", file=args["output"])
        else:
            print(ext,
                  tig2posread[tig][-2][2],
                  tig2posread[tig][-2][5],
                  ((tig[1] - tig2posread[tig][-2][1]) - tig2posread[tig][-2][3]) * -1,
                  sep=",", file=args["output"])

if __name__ == '__main__':
    main(sys.argv[1:])

