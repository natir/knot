#!/usr/bin/env python3

# std import
import os
import csv
import sys
import argparse
import subprocess

from jinja2 import FileSystemLoader
from jinja2 import Environment

from Bio import SeqIO

def main(args=None):

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(prog="knot.analysis.generate_report")

    parser.add_argument("-i", "--input_prefix", type=str, help="prefix of knot output", required=True)
    parser.add_argument("-o", "--output", type=argparse.FileType('wb'), help="path where report was write", required=True)
    
    parser.add_argument("-c", "--classification", help="Add path classification in report", action="store_true")
    parser.add_argument("-p", "--hamilton-path", help="Add hamilton path in report", action="store_true")

    args = vars(parser.parse_args(args))

    template_path = os.path.dirname(__file__) + os.sep + "template" + os.sep
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template('report.jinja2.html')

    param = dict()
    
    contig_info(param, open(args["input_prefix"] + "knot/contigs.fasta"))

    if args["classification"]:
        run_classification(args["input_prefix"] + "AAG.csv", args["input_prefix"])
        classification_info(param, open(args["input_prefix"]+"classification.csv"))

    if args["hamilton_path"]:
        run_hamilton(args["input_prefix"] + "AAG.csv", args["input_prefix"])
        hamilton_info(param, open(args["input_prefix"]+"hamilton_path.csv"))
    
    full_aag_info(param, open(args["input_prefix"]+"AAG.csv"))

    build_AAG_representation(param, open(args["input_prefix"]+"AAG.csv"))
        
    args["output"].write(template.render(param).encode("utf-8"))

def contig_info(param, contig_file):

    tig2len = dict()
    for record in SeqIO.parse(contig_file, "fasta"):
        tig2len[record.id] = len(record.seq)

    param["tig_info"] = tig2len

def run_classification(aag_path, prefix_output):
    subprocess.run(["knot.analysis.classifications", "-i", aag_path, "-o", prefix_output+"_classification.csv"])
    
def classification_info(param, classification_file):

    ext2type = dict()
    for row in csv.DictReader(classification_file):
        ext2type[(row["ext1"], row["ext2"])] = row["type"]

    param["classification_info"] = ext2type

def run_hamilton(aag_path, prefix_output):
    subprocess.run(["knot.analysis.hamilton_path", "-i", aag_path, "-o", prefix_output+"_hamilton_path.csv"])

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
        nodes += "{{ id: '{}_begin', label: 'begin' }},\n".format(tig, tig)
        nodes += "{{ id: '{}_end', label: 'end' }},\n".format(tig, tig)
        
    for tig in tig_set:
        e1 = tig + "_begin"
        e2 = tig + "_end"
        edges += "{{from: '{}', to: '{}', label: '{}', width: 10, length: 1}},\n".format(e1, e2, tig)
        
    param["aag_nodes"] = nodes
    param["aag_edges"] = edges

if __name__ == "__main__":
    main()
