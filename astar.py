import osmnx as ox
import pickle
import networkx as nx
import heapq
import math


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


def get_node_distance(graph, n1, n2):
    pass


# based on pseudocode from: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
def astar(graph: nx.Graph, source: int, target: int):

    #iteration count
    iter = 0

    # priority queue
    Q = []

    # preallocating a distance matrix
    dist = [math.inf] * graph.number_of_nodes()
    dist[source] = 0

    # previous node matrix
    prev = [-1] * graph.number_of_nodes()

    # heap arr, (priority, value)
    heapq.heappush(Q, (0, source))

    #lat and long of target for use in A* heuristic
    target_lat = graph.nodes[target]['y']
    target_lon = graph.nodes[target]['x']

    while len(Q) > 0:
        iter += 1
        _, u = heapq.heappop(Q)
        for _, v, data in graph.edges(u, data=True):
            weight = data['length']
            #this is the A* additon, the heuristic
            h = ox.distance.great_circle(target_lat, target_lon, graph.nodes[v]['y'], graph.nodes[v]['x'])
            if dist[v] > dist[u] + weight + h:
                dist[v] = dist[u] + weight
                heapq.heappush(Q, (dist[v] + h, v))
                # store the predecessor node that results in shortest path to source
                prev[v] = u

                # if we've found the node we're looking for...
                if (v == target):
                    # stop the search by clearning the queue
                    Q.clear()
                    # exit loop through neighbors
                    print("iterations: ", iter)
                    break

    # backtracked shortest path
    backtrack = []
    # if target was found...
    if (prev[target] != -1):
        u = target
        while u != -1:
            # add node to shortest_path
            backtrack.append(u)
            # move to next node in chain
            u = prev[u]

    route = []
    # reverse the list, using stuff I actually learned in DSA!
    while (backtrack):
        route.append(backtrack.pop())

    return route


def main():
    graph = get_city_graph("Jacksonville, Florida")
    graph = nx.convert_node_labels_to_integers(graph, first_label=0, label_attribute='original_label')
    # graph = nx.Graph(ox.project_graph(nx.MultiDiGraph(graph)))
    print(f"Nodes: {graph.number_of_nodes()}, Edges {graph.number_of_edges()}")

    route = astar(graph, 6000, 150)

    ox.plot.plot_graph_route(nx.MultiDiGraph(graph), route)


if __name__ == "__main__":
    main()