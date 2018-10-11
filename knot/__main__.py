#!/usr/bin/env python3

# std import
import io
import os
import csv
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
        import sys
        args = sys.argv[1:]

    parser = MyArgumentParser(prog="KNOT")

    # avaible
    # b e g i j m o q u w x y z
    # A B C E G H I J K L M N Q V W X Y Z
    parser.add_argument("-C", "--contigs", required=True,
                        help="fasta file than contains contigs")
    parser.add_argument("-g", "--graph", required=True,
                        help="contig graph")
    parser.add_argument("-i", "--input", required=True,
                        help="read used for assembly")
    parser.add_argument("--read-type", choices=["pb", "ont"], default="pb",
                        help="type of input read, default pb")
    parser.add_argument("--clean", action="store_true")

    args, unknow_arg = parser.parse_known_args(args)
    args = vars(args)

    package_path = os.path.dirname(__file__) + os.sep
    snakemake_rule = os.path.join(package_path, "report.rules")
    snakemake_config_path = os.path.join(package_path, "config.yaml")

    call = ["snakemake", "report",
            "--configfile", snakemake_config_path,
            "--config",
            "input="+args["input"],
            "graph="+args["graph"],
            "contigs="+args["contigs"],
            "read_type="+args["read_type"],
            "package_path="+package_path,
            "--snakefile", snakemake_rule
            ]

    if args["clean"]:
        call.append("-S")
        out = subprocess.run(call, stdout=subprocess.PIPE)
        
        fakefile = io.StringIO(str(out.stdout.decode("utf-8")))
        fakefile.seek(0)
        
        reader = csv.reader(fakefile, delimiter="\t")
        next(reader)
        for row in reader:
            if row[0] != args["graph"]: #don't remove input
                rm_out = subprocess.run(["rm", "-rf", row[0]])
        return

    call += unknow_arg
    
    out = subprocess.call(call)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
