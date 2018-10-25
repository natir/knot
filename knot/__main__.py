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

# Class to call help and snakemake help
class MyArgumentParser(argparse.ArgumentParser):
    def print_help(self):
        super().print_help()
        print()
        subprocess.run(["snakemake", "--help"])


def main(args = None):

    if args is None:
        args = sys.argv[1:]

    parser = MyArgumentParser(prog="KNOT")

    # avaible
    # b e g i m o q u w x y z
    # A B C E G H I J K L M N Q V W X Y Z
    parser.add_argument("-C", "--contigs", required=True,
                        help="fasta file than contains contigs")
    parser.add_argument("-g", "--contigs_graph",
                        help="contigs graph")
    parser.add_argument("-i", "--raw-reads",
                        help="read used for assembly")
    parser.add_argument("-m", "--correct-reads",
                        help="read used for assembly")
    parser.add_argument("-o", "--output", required=True,
                        help="output prefix")
    parser.add_argument("--read-type", choices=["pb", "ont"], default="pb",
                        help="type of input read, default pb")

    args, unknow_arg = parser.parse_known_args(args)
    args = vars(args)

    # Check parameter
    ## raw_reads or correct
    go_out = False
    if args["raw_reads"] is None and args["correct_reads"] is None:
        print("You need set --raw-reads or --correct-reads\n", file=sys.stderr)
        go_out = True
    
    if args["raw_reads"] is not None and args["correct_reads"] is not None:
        print("You can't set --raw-reads and --correct-reads at same time\n", file=sys.stderr)
        go_out = True

    if go_out:
        parser.print_help()
        sys.exit(1)

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
            "package_path="+package_path,
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

    call += unknow_arg
    
    print(" ".join(call))
    out = subprocess.call(call)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
