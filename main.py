import configparser
import math
import os
import random


class Config:
    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        self.directed = config["GRAPH"].getboolean("directed")
        self.max_weight = int(config["GRAPH"]["max_weight"])
        self.min_weight = int(config["GRAPH"]["min_weight"])
        self.num_nodes = int(config["GRAPH"]["num_nodes"])
        self.weighted = config["GRAPH"].getboolean("weighted")
        self.alpha = float(config["GRAPH"]["alpha"])
        self.beta = float(config["GRAPH"]["beta"])
        self.output_gv_name = config["GRAPH"]["output_gv_name"]


def main(config_file):
    config = Config(config_file)
    graph = create_graph(config)
    print(config.num_nodes, len(graph))
    for edge in graph:
        print(*edge)
    to_graphviz(graph, config)


def create_graph(config):
    num_nodes = config.num_nodes

    # assume it is undirected. The max number of edges is (n*(n-1))/2
    max_edges = (num_nodes * (num_nodes - 1)) // 2
    min_edges = num_nodes - 1
    if config.directed:
        # if it's directed, just double that number
        max_edges *= 2
        min_edges = ((num_nodes-1)*(num_nodes-2)) + 1
    num_edges = random_num_edges(min_edges, max_edges, config.alpha, config.beta)
    edges = set()
    while len(edges) < num_edges:
        from_node = random.randrange(num_nodes)
        to_node = random.randrange(num_nodes)

        # guarantee no self edges
        while from_node == to_node:
            to_node = random.randrange(num_nodes)

        if config.directed:
            new_edge = (from_node, to_node)
            if new_edge not in edges:
                edges |= {new_edge}
        else:
            new_edge1 = (from_node, to_node)
            new_edge2 = (to_node, from_node)
            if (new_edge1 not in edges) and (new_edge2 not in edges):
                # pick one at random
                edges |= {new_edge1}

    if not config.weighted:
        return edges

    # otherwise, add the weights
    weighted_edges = set()
    for edge in edges:
        weight = random.randint(config.min_weight, config.max_weight)
        weighted_edge = (*edge, weight)
        weighted_edges |= {weighted_edge}

    return weighted_edges


def random_num_edges(min_edges, max_edges, alpha, beta):
    selector = random.betavariate(alpha, beta)
    edge_range = max_edges - min_edges + 1
    return math.floor(edge_range * selector) + min_edges


def to_graphviz(graph, config):
    name = config.output_gv_name
    filename = name + ".gv"
    with open(filename, "w") as f:
        edgeop = "--"
        graph_type = "graph"
        if config.directed:
            edgeop = "->"
            graph_type = "digraph"

        f.write("{} {} {{\n".format(graph_type, name))
        f.write("  0 [style=filled,fillcolor=green]\n")
        f.write("  {} [style=filled,fillcolor=red]\n".format(config.num_nodes-1))
        for edge in graph:
            if config.weighted:
                # Flip the weight. For some reason, graphviz thinks that larger
                # weights should correlate to shorter edges
                weight = config.max_weight - edge[2] + config.min_weight
                f.write("  {} {} {} [weight={},label={}]\n".format(edge[0],
                    edgeop, edge[1], weight, edge[2]))
            else:
                f.write("  {} {} {} [weight=1]\n".format(edge[0], edgeop, edge[1]))
        f.write("}\n")


if __name__ == "__main__":
    if len(os.sys.argv) == 2:
        main(os.sys.argv[1])
    else:
        main("config.ini")
