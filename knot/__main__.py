#!/usr/bin/env python3

# std import
import io
import os
import csv
import sys
import tempfile
import argparse
import subprocess

# project import

# print snakemake help
def snakemake_help(p):
    subprocess.run(["snakemake", "--help"])

def main(args = None):

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(prog="KNOT")

    parser.add_argument("-c", "--contigs", required=True,
                        help="fasta file than contains contigs")
    parser.add_argument("-g", "--contigs_graph",
                        help="contigs graph")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-r", "--raw-reads",
                        help="read used for assembly")
    group.add_argument("-C", "--correct-reads",
                        help="read used for assembly") 
   
    parser.add_argument("-o", "--output", required=True,
                        help="output prefix")
    parser.add_argument("--contig-min-length", default=100000, type=int,
                        help="contig with size lower this parameter are ignored")
    parser.add_argument("--read-type", choices=["pb", "ont"], default="pb",
                        help="type of input read, default pb")
    parser.add_argument("--help-all", action='store_true',
                        help="show knot help and snakemake help")
    args, unknow_arg = parser.parse_known_args(args)
    args = vars(args)
    
    # Check parameter
    ## raw_reads or correct
    if args["help_all"]:
        parser.print_help()
        snakemake_help()
        return 1

    ## if contig graph isn't set generate empty file
    if args["contigs_graph"] is None:
        args["contigs_graph"] = tempfile.NamedTemporaryFile(delete=False).name

    package_path = os.path.dirname(__file__) + os.sep
    snakemake_rule = os.path.join(package_path, "main.rules")
    snakemake_config_path = os.path.join(package_path, "config.yaml")

    config = [
        "contigs="+args["contigs"],
        "out_prefix="+args["output"],
        "contigs_graph="+args["contigs_graph"],
        "read_type="+args["read_type"],
        "min_contig_length="+str(args["contig_min_length"]),
        "package_path="+package_path
    ]

    if args["raw_reads"] is not None:
        config.append("raw_reads="+args["raw_reads"])
    else:
        config.append("correct_reads="+args["correct_reads"])

    call = ["snakemake", args["output"] + "_AAG.csv",
            "--configfile", snakemake_config_path,
            "--config",
            *config,
            "--snakefile", snakemake_rule
    ]

    call += unknow_arg[1:]
    
    print(" ".join(call))
    out = subprocess.call(call)

    return 0
    
if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
