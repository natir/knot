#!/usr/bin/env python3

# std import
import os
import csv
import sys
import argparse

from jinja2 import FileSystemLoader
from jinja2 import Environment

from Bio import SeqIO

def main(args=None):

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(prog="knot.analysis.generate_report")

    parser.add_argument("-a", "--aag", type=argparse.FileType('r'), help="AAG filepath")
    parser.add_argument("-C", "--contig", type=argparse.FileType('r'), help="contig filepath", required=True)
    parser.add_argument("-c", "--classification", type=argparse.FileType('r'), help="path classification filepath", required=True)
    parser.add_argument("-p", "--hamilton-path", type=argparse.FileType('r'), help="hamilton path filepath")
    parser.add_argument("-o", "--output", type=argparse.FileType('wb'), help="path where report was write")

    args = vars(parser.parse_args(args))
    
    template_path = os.path.dirname(__file__) + os.sep + "template" + os.sep
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template('report.jinja2.html')

    param = dict()
    
    contig_info(param, args["contig"])
    classification_info(param, args["classification"])

    if args["hamilton_path"] is not None:
        hamilton_info(param, args["hamilton_path"])
    
    full_aag_info(param, args["aag"])
    args["aag"].seek(0)
    build_AAG_representation(param, args["aag"])
        
    args["output"].write(template.render(param).encode("utf-8"))

def contig_info(param, contig_file):

    tig2len = dict()
    for record in SeqIO.parse(contig_file, "fasta"):
        tig2len[record.id] = len(record.seq)

    param["tig_info"] = tig2len

def classification_info(param, classification_file):

    ext2type = dict()
    for row in csv.DictReader(classification_file):
        ext2type[(row["ext1"], row["ext2"])] = row["type"]

    param["classification_info"] = ext2type

def hamilton_info(param, hamilton_file):

    hamilton_path = list()
    for row in csv.reader(hamilton_file, delimiter=";"):
        hamilton_path.append((list(row[0].split(",")), row[1]))

    param["hamilton_info"] = hamilton_path

def full_aag_info(param, aag_file):

    aag_record = list()
    for row in csv.DictReader(aag_file):
        aag_record.append((row["tig1"], row["tig2"], row["nb_base"], row["nb_read"], row["nbread_contig"].split(";"), row["read1"], row["read2"]))

    param["full_aag_info"] = aag_record

def build_AAG_representation(param, aag_file):
    nodes = "" 
    edges = ""

    edges_dict = dict()
    tig_set = set()
    for row in csv.DictReader(aag_file):
        tig_set.add(row["tig1"].split("_")[0])
        tig_set.add(row["tig2"].split("_")[0])

        key = frozenset((row["tig1"], row["tig2"]))

        if row["paths"] == "not_found":
            continue
        
        if key in edges_dict and edges_dict[key] < int(row["nb_base"]):
            continue

        edges_dict[frozenset((row["tig1"], row["tig2"]))] = int(row["nb_base"])

    for (tig1, tig2), length in edges_dict.items():
        if length <= 0:
            length = "overlap"
        edges += "{{ from: '{}', to: '{}', label: '{}', id: '{}' }},\n".format(tig1, tig2, length, tig1+"-"+tig2)

        
    for tig in tig_set:
        nodes += "{{ id: '{}_begin', label: '{}_begin' }},\n".format(tig, tig)
        nodes += "{{ id: '{}_end', label: '{}_end' }},\n".format(tig, tig)
        
    for tig in tig_set:
        e1 = tig + "_begin"
        e2 = tig + "_end"
        edges += "{{from: '{}', to: '{}', label: '{}', width: 10, length: 1}},\n".format(e1, e2, tig)
        
    param["aag_nodes"] = nodes
    param["aag_edges"] = edges

if __name__ == "__main__":
    main()
