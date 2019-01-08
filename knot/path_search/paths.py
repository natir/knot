# std import
import logging
from collections import Counter

# pip import
import networkx as nx

def get_path(graph, n1, n2, mode="base"):

    try:
        if mode == "base":
            path = nx.shortest_path(graph, n1, n2, weight="weight")
        else:
            path = nx.shortest_path(graph, n1, n2)
    except nx.exception.NetworkXError as e:
        logging.debug("Networkx exception"+str(e))
        path = []
    except nx.exception.NetworkXNoPath as e:
        logging.debug("No path exception "+str(e))
        path = []
    except nx.exception.NodeNotFound as e:
        logging.debug("Node not found exception "+str(e))
        path = []

    return path, sum([graph.edges[x, y]["weight"] for x, y in zip(path, path[1:])])

def path_through_contig(tig2reads, path):
    tig2nb_read = Counter()

    for node in path:
        tig2nb_read[get_tig_read(tig2reads, node)] += 1

    return tig2nb_read

def get_tig_read(tig2reads, read):
    read = read[:-1]
    for tig, reads in tig2reads.items():
        if read in reads:
            return tig

    return None

def format_node_contig_counter(node_contig_counter, tig2reads):
    result = list()

    for key, count in node_contig_counter.items():
        if key in tig2reads:
            nb_read, tig_name = len(tig2reads[key]), key
        else:
            nb_read, tig_name = 0, "not_assign"

        result.append("{}:{}/{}".format(tig_name, count, nb_read))

    return ";".join(result)
