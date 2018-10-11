# std import
import logging

# pip import
import gfapy 
import networkx as nx

# project import

def get_sg(gfa_file):
    # Convert gfa in SG
    logging.info("begin parseGFA")
    graph = read_gfa_from_handler(gfa_file)
    logging.info("end parseGFA")

    G = nx.DiGraph()
    logging.info("populate graph begin")
    populate_graph(graph, G)
    logging.info("populate graph end")

    print_info(G)
    
    logging.info("transitive reduction begin")
    G = transitive_reduction(G)
    logging.info("transitive reduction end")
    
    nb_trans = check_trans_red(G)
    if nb_trans > 0:
        logging.warning("Nb error in transitive reduction "+str(nb_trans))

    print_info(G)

    return G

def read_gfa_from_handler(handler):
    gfa = gfapy.Gfa()

    for line in handler:
        gfa.append(line)

    return gfa

def populate_graph(gfa, G): 
   
    is_contain = isContain(gfa)

    for d in gfa.dovetails:
        __add_dovetails(d, G, is_contain)
        __add_dovetails(d.complement(), G, is_contain)

def __add_dovetails(d, G, is_contain):
    G.add_node(d.from_name + d.from_orient, containment=is_contain(d.from_name))
    G.add_node(d.to_name + d.to_orient, containment=is_contain(d.to_name))

    if d.NM is None or d.om is None or d.om == 0:
        qual_val = 0.0
    else:
        qual_val = (d.NM / d.om) * 100.0

    G.add_edge(d.from_name + d.from_orient,
               d.to_name + d.to_orient,
               qual=qual_val,
               len=d.alignment.length_on_query(),
               overhang_len=d.to_segment.length - d.alignment.length_on_query(),
               overhang_maplen=d.get("om"),
               weight=1)

class isContain:
    
    def __init__(self, gfa):
        self.containment2pos = {l.to_name: i for i, l in enumerate(gfa.containments)}

    def __call__(self, node):
        return node in self.containment2pos

    def index(self, node):
        return self.containment2pos[node]

def print_info(G):
    logging.debug("begin transitiv reduction")
    logging.debug("nb edge : " + str(G.number_of_edges()))
    logging.debug("nb node : " + str(G.number_of_nodes()))
    logging.debug("nb strong components : " + str(nx.number_strongly_connected_components(G)))
    logging.debug("nb weak components : " + str(nx.number_weakly_connected_components(G)))

def check_trans_red(G):
    nb_error = 0
    for x in G.nodes():
        for y in G.successors(x):
            for z in (set(G.successors(x)) & set(G.successors(y))):
                nb_error += 1

    return nb_error

def transitive_reduction(G):
    FUZZ = 10

    edge_eliminate = set()
    inplay_node = set()

    for v in G.nodes():
        eliminated_node = set()
        
        for w in G.successors(v):
            inplay_node.add(w)
       
        if len(list(G.successors(v))) == 0:
            continue
        longest = max([data["overhang_len"] for v, w, data in G.edges(v, data=True)]) + FUZZ

        for _, w, vw_len in get_edge_in_len_order(G, v):
            for _, x, wx_len in get_edge_in_len_order(G, w):
                if vw_len + wx_len > longest:
                    break
 
                if x in inplay_node:
                    eliminated_node.add(x)

        for _, w, vw_len in get_edge_in_len_order(G, v): 
            nb_edge_inf_fuzz = 0
            for _, x, wx_len in get_edge_in_len_order(G, w):
                if wx_len > FUZZ:
                    break

                if x in inplay_node :
                    eliminated_node.add(x)
                    inplay_node.remove(x)
                    nb_edge_inf_fuzz +=1

            if nb_edge_inf_fuzz == 0:
                try:
                    x = next(get_edge_in_len_order(G,w))[1]
                    eliminated_node.add(x)
                except StopIteration:
                    # w have no successor
                    pass

        for w in G.successors(v):
            if w in eliminated_node:
                edge_eliminate.add((v, w))
                eliminated_node.remove(w)
            inplay_node.discard(w)

    [G.remove_edge(v, w) for v, w in edge_eliminate]
    
    return G

def get_edge_in_len_order(G, v):
    for v, w, edge_len in sorted([(v, w, G.get_edge_data(v, w)["overhang_len"]) 
                                      for w in G.successors(v)], 
                                  key=lambda tup: tup[2]):
        yield (v, w, edge_len)

