
import osmnx as ox
import pickle
import networkx as nx

def get_city_graph(city_string) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
    try:
        print("Looking for cached graph...")
        with open(f'{city_string}.pkl', 'rb') as f:
            print("Found cached graph!")
            graph = pickle.load(f)
    except:
        print("No cached graph found, downloading (this might take a while)...")
        graph = ox.graph.graph_from_place(city_string)
        #print("Converting graph to simple format...")
        #graph = convert_to_simple_graph(graph)
        print("Saving graph to cache...")
        with open(f'{city_string}.pkl', 'wb') as f:
            pickle.dump(graph, f)
    return graph

# a helper function I wrote to speed up graph saving
def graph_to_pickle(city_string):
    graph = ox.load_graphml(f"{city_string}.graphml")
    simple_graph = convert_to_simple_graph(graph)
    with open(f'{city_string}.pkl', 'wb') as f:
            pickle.dump(simple_graph, f)

# converts to undirected graph with one connection between nodes
def convert_to_simple_graph(graph: nx.MultiDiGraph) -> nx.Graph:
    simple_graph = nx.Graph(graph)
    return simple_graph
