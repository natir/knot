# std import
import csv

from collections import defaultdict

def get_valid_read(read2read):
    read_out = set()
    read_in = set()

    not_valid = set()

    reader = csv.reader(read2read, delimiter="\t")
    for row in reader:
        if row[0] == "S" and int(row[3].split(":")[2]) < 2000:
            not_valid.add(row[1])

        if row[0] == "L" and row[0] not in not_valid:
            read_out.add(row[1])
            read_in.add(row[3])
    
    return read_out & read_in

def get_tig2posread(read2tig, valid_read):
    result = defaultdict(list)

    reader = csv.reader(read2tig, delimiter="\t")
    for row in reader:
        if valid_read and row[0] not in valid_read:
            continue
        if int(row[3]) - int(row[2]) > 0.7 * int(row[1]):
            result[(row[5], int(row[6]))].append((int(row[7]), int(row[8]), row[0], row[4]))

    return result

