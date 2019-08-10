import configparser
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


def main(config_file):
    config = Config(config_file)
    graph = create_graph(config)
    print(config.num_nodes, len(graph))
    for edge in graph:
        print(*edge)


def create_graph(config):
    num_nodes = config.num_nodes

    # assume it is undirected. The max number of edges is (n*(n-1))/2
    max_edges = (num_nodes * (num_nodes - 1)) // 2
    min_edges = num_nodes - 1
    if config.directed:
        # if it's directed, just double that number
        max_edges *= 2
        min_edges = ((num_nodes-1)*(num_nodes-2)) + 1
    num_edges = random.randint(min_edges, max_edges)
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


if __name__ == "__main__":
    if len(os.sys.argv) == 2:
        main(os.sys.argv[1])
    else:
        main("config.ini")
