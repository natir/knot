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
        if row[0] not in valid_read:
            continue
        if int(row[3]) - int(row[2]) > 0.7 * int(row[1]):
            result[row[5]].append((int(row[7]), row[8], row[4]))

    return result

