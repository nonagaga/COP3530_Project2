import osmnx as ox
import networkx as nx
import pickle
import math

#helper function written by Gabriel Wagner
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
        print("Converting graph to simple format...")
        simple_graph = convert_to_simple_graph(graph)
        print("Saving graph to cache...")
        with open(f'{city_string}.pkl', 'wb') as f:
            pickle.dump(simple_graph, f)
    return graph

#helper function written by Gabriel Wagner
def graph_to_pickle(city_string):
    graph = ox.load_graphml(f"{city_string}.graphml")
    simple_graph = convert_to_simple_graph(graph)
    with open(f'{city_string}.pkl', 'wb') as f:
            pickle.dump(simple_graph, f)

#helper function written by Gabriel Wagner
def convert_to_simple_graph(graph: nx.MultiDiGraph) -> nx.Graph:
    simple_graph = nx.Graph(graph)
    return simple_graph

def bellman_ford(graph: nx.Graph, source: int, target: int):
    #create a data structure to store the length from selected node to each final node
    dist = [math.inf] * graph.number_of_nodes()
    dist[source] = 0
    predecessor = [None] * graph.number_of_nodes()

    #Iterate n-1 times
    for i in range(graph.number_of_nodes()-1):
        updated = False
        #iterate through all edges and update lengths to each node
        for (u, v, w) in graph.edges.data("length"):
            if dist[u] + w < dist[v]:
                #updated = True
                dist[v] = dist[u] + w
                predecessor[v] = u
        #if not updated:
            #break

    #create the path by accessing the predecessors
    backtrack = []
    curr_node = target
    while curr_node != source:
        print("successful backtrack")
        backtrack.append(predecessor[curr_node])
        curr_node = predecessor[curr_node]

    #reverse the path to create the route
    route = []
    while (backtrack):
        route.append(backtrack.pop())

    return route



def main():
    graph = get_city_graph("Jacksonville, Florida")
    graph = nx.convert_node_labels_to_integers(graph)
    print(f"Nodes: {graph.number_of_nodes()}, Edges {graph.number_of_edges()}")

    route = bellman_ford(graph, 0, len(graph) - 1)

    ox.plot.plot_graph_route(nx.MultiDiGraph(graph), route)

if __name__ == "__main__":
    main()