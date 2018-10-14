# std import
import csv

from collections import defaultdict

def get_valid_read(read2read):
    result = set()
    
    reader = csv.reader(read2read, delimiter="\t")
    for row in reader:
        if row[0] == "L":
            result.add(row[1])
            result.add(row[3])
    
    return result

def get_tig2posread(read2tig, valid_read):
    result = defaultdict(list)

    reader = csv.reader(read2tig, delimiter="\t")
    for row in reader:
        if row[5] not in valid_read:
            continue
        if int(row[8]) - int(row[7]) > 0.7 * int(row[6]):
            result[row[0]].append((int(row[2]), row[5], row[4]))

    return result

