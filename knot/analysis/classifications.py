#!/usr/bin/env python3

# std import
import csv
import sys
import argparse
from collections import Counter

def main(args=None):

    #argument parsing
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(prog="knot.analysis.classifications")

    parser.add_argument("-i", "--input", type=argparse.FileType('r'), help="path to the AAG", required=True)
    parser.add_argument("-o", "--output", type=argparse.FileType('w'), help="path where classification report was write", required=True)
    parser.add_argument("-t", "--threshold", type=int, default=10000, help="path length threshold")

    args = vars(parser.parse_args(args))

    paths = dict()

    reader = csv.DictReader(args["input"])
    for row in reader:
        key = frozenset((row["tig1"], row["tig2"]))

        if row["paths"] == "not_found":
            continue
        
        if row["paths"] == "not_search":
            nb_base = 0
        else:
            nb_base = int(row["nb_base"])
            
        # keep only the shortest path
        if key in paths and paths[key]["nb_base"] < nb_base:
            continue

        paths[key] = dict()
        paths[key]["nb_base"] = nb_base
        paths[key]["adjacent"] = adjacent_len(nb_base, args["threshold"]) and adjacent_tig(row["nbread_contig"], key)
            
    counter = Counter()
    for key in paths:
        if paths[key]["adjacent"]:
            for k in key:
                counter[k] += 1

    multi_adjacent = {k for k, count in counter.items() if count > 1}

    for key in paths:
        if not paths[key]["adjacent"]:
            path_type = "distant"
        elif any([k in multi_adjacent for k in key]):
            path_type = "multiple adjacency"
        else:
            path_type = "single adjacency"
            
        print("{},{}".format(path_type, "-".join(key)), file=args["output"])
        
def adjacent_len(length, threshold):
    return int(length) <= threshold

def adjacent_tig(nb_contig, pair_tig):
    nb_contig = nb_contig.split(";")

    pair_tig = {v.split("_")[0] for v in pair_tig}
    pair_tig.add("not_assign")
    
    for contig in nb_contig:
        contig = contig.split(":")
        if contig[0] not in pair_tig:
            return False

    return True
    
if __name__ == "__main__":
    main()
