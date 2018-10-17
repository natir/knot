#!/usr/bin/env python3

# std import
import csv
import sys
import logging
import argparse
import itertools

# project import
from knot import path_search 
from knot import extremity_search 
from knot.path_search import paths
from knot.path_search import gfa2sg

# Logging configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s :: %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

def main(args=None):

    # argument parsing
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(prog="knot.path_search",
                                     formatter_class=argparse.
                                     ArgumentDefaultsHelpFormatter)

    parser.add_argument("search", type=argparse.FileType('r'))
    parser.add_argument("result", type=argparse.FileType('w'))
    parser.add_argument("ovl_graph", type=argparse.FileType('r'))
    parser.add_argument("read2asm", type=argparse.FileType('r'))
    parser.add_argument("asm_graph", type=argparse.FileType('r'))
    parser.add_argument("tig2tig", type=argparse.FileType('r'))

    args = vars(parser.parse_args(args))

    # gfa to sg
    sg = gfa2sg.get_sg(args["ovl_graph"])
    args["ovl_graph"].seek(0)
    
    # get info about contig
    valid_read = extremity_search.get_valid_read(args["ovl_graph"])
    tig2reads = {tig: {v[2] for v in val} for tig, val in extremity_search.get_tig2posread(args["read2asm"], valid_read).items()}
   

    # build list of search
    tig_ext = list()
    reader = csv.DictReader(args["search"])
    for row in reader:
        tig_ext.append(tuple(row.values()))

    print("tig1", "read1", "tig2", "read2", "path_len", "nbread_contig",
          sep=",", file=args["result"])

    no_search = path_search.get_ext_ovl(args["asm_graph"], args["tig2tig"]) 

    for ext1, ext2 in itertools.permutations(tig_ext, 2):
        if ext1[0][:-6] == ext2[0][:-4] or ext1[0][:-4] == ext2[0][:-6]:
            continue # don't search path between same contig ext

        if(ext1, ext2) in no_search:
            print(ext1,"no",ext2,"no",0,"", sep=",", file=args["result"])

        node1 = ext1[1] + "-" if ext1[2] == "+" else ext1[1] + "+"
        node2 = ext2[1] + "-" if ext2[2] == "+" else ext2[1] + "+"

        path = paths.get_path(sg, node1, node2)
        if path:
            nbread_contig = paths.format_node_contig_counter(
                paths.path_through_contig(tig2reads, path),
                tig2reads)

            print(ext1[0], node1, ext2[0], node2, len(path), nbread_contig,
                  sep=",", file=args["result"])


if __name__ == "__main__":
    main()
