import osmnx as ox
import networkx as nx
import heapq
import math
from utils import get_city_graph

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
            if dist[v] > dist[u] + weight:
                dist[v] = dist[u] + weight
                # heuristic only affects the ordering in the priority queue
                heapq.heappush(Q, (dist[v] + h, v))
                # store the predecessor node that results in shortest path to source
                prev[v] = u

                # if we've found the node we're looking for...
                if (v == target):
                    # stop the search by clearning the queue
                    Q.clear()
                    # exit loop through neighbors
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

    return route, dist[target], iter


def main():
    graph = get_city_graph("Jacksonville, Florida")
    graph = nx.convert_node_labels_to_integers(graph, first_label=0, label_attribute='original_label')
    print(f"Nodes: {graph.number_of_nodes()}, Edges {graph.number_of_edges()}")

    route, dist, iter = astar(graph, 6000, 150)

    ox.plot.plot_graph_route(nx.MultiDiGraph(graph), route)


if __name__ == "__main__":
    main()