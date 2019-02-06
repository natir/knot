#!/usr/bin/env python3

# std import
import csv
import sys
import argparse

# pip import
import itertools
import networkx as nx

def main(args=None):

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(prog="knot.analysis.classifications")
           
    parser.add_argument("-i", "--input", type=argparse.FileType('r'), help="path to the AAG", required=True)
    parser.add_argument("-o", "--output", type=argparse.FileType('w'), help="path where hamilton path was write", required=True)
    parser.add_argument("-c", "--circular", action="store_true", help="genome is circular")
    
    args = vars(parser.parse_args(args))

    graph = AAG2graph(args["input"])

    paths = []
    for cycle in valid_cycle(graph, args["circular"]):
        weight = sum([graph.edges[edge[0], edge[1]]["weight"] for edge in cycle])

        nodes = ",".join(remove_duplicate_if_follow([e for edge in cycle for e in edge]))
        paths.append((weight, nodes))

    paths.sort()

    for (weight, nodes) in paths:
        print(";".join([nodes, str(weight)]), file=args["output"])

def remove_duplicate_if_follow(l):
    previous = None
    for elt in l:
        if elt == previous:
            previous = elt
            continue

        previous = elt
        yield elt
        
def valid_cycle(graph, circular_genome=False):
    for g in itertools.permutations(graph.nodes()):
        if not contig_congruence(g):
            continue

        if g.index(min(g)) != 0:
            continue

        if circular_genome:
            edges = [edge for edge in zip(g, g[1:] + g[:1])]
        else:
            edges = [edge for edge in zip(g, g[1:])]

        if any([edge not in graph.edges for edge in edges]) :
            continue
                
        yield edges

def contig_congruence(g):
    for i, j in zip(g[::2], g[1::2]):
        if i.split("_")[0] != j.split("_")[0]:
            return False
    return True
            
def AAG2graph(AAG_path):

    paths = dict()
    reader = csv.DictReader(AAG_path)
    for row in reader:
        key = frozenset((row["tig1"], row["tig2"]))
        
        if row["paths"] == "not_found":
            continue

        if row["paths"] == "not_search":
            nb_base = 0
        else:
            nb_base = int(row["nb_base"])

        if key in paths and paths[key] < nb_base:
            continue

        paths[key] = nb_base

    graph = nx.DiGraph()
    for (tig1, tig2), nb_base in paths.items():
        graph.add_edge(tig1, tig2, weight=nb_base)
        graph.add_edge(tig2, tig1, weight=nb_base)

    tig_in_graph = set()
    for key in paths.keys():
        for k in key:
            tig_in_graph.add(k.split("_")[0])

    for tig in tig_in_graph:
        graph.add_edge(tig+"_begin", tig+"_end", weight=0)
        graph.add_edge(tig+"_end", tig+"_begin", weight=0)

    return graph
        
if __name__ == "__main__":
    main()
