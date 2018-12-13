
def get_ext_ovl(asm_graph, tig2tig):
    result = set()

    signe2pos = {"-": "begin", "+": "end", "begin": "-", "end": "+"}

    for row in asm_graph:
        row = row.strip().split('\t')
        if row[0] == "L":
            result.add(__gfa_line_parse(row))
    
    for row in tig2tig:
        row = row.strip().split('\t')
        if row[0] == "L":
            result.add(__gfa_line_parse(row))

    return result

def __gfa_line_parse(row):
    first_suffix = "_end"
    if row[2] == '-':
        first_suffix = "_begin"
   
    second_suffix = "_begin"
    if row[2] == '-':
        second_suffix = "_end"

    return (row[1]+first_suffix, row[3]+second_suffix)

def choose_read_ori(read, ori, pos, source):
    """
    To much magique her:
    read: read id
    ori: orientation of read on contig
    pos: at begin or end of contig
    source: this read are source of search or not
    """
    if source:
        if pos == "begin":
            if ori == "+":
                return read + "-"
            else:
                return read + "+"
        else:
            if ori == "+":
                return read + "+"
            else:
                return read + "-"
    else:
        if pos == "begin":
            if ori == "+":
                return read + "+"
            else:
                return read + "-"
        else:
            if ori == "+":
                return read + "-"
            else:
                return read + "+"
