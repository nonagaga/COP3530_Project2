import networkx as nx

from dijkstra import *
import random
import time
from astar import astar
import matplotlib.pyplot as plt

def main():
    graph = None
    alg = None
    while True:
        print("Enter City Name: ")
        city = input()
        print("\nEnter State: ")
        state = input()

        try:
            graph = get_city_graph(f'{city}, {state}')
        except:
            print("\nCity and State combination not found, try again\n")
            continue
        '''while True:
            print("Which algorith would you like to use?(Type Dijkstra or A*)\n")
            alg = input()
            if alg != 'Dijkstra' and alg != 'A*':
                print("Invalid Algorithm\n")
                continue
            break'''
        break
    graph = nx.convert_node_labels_to_integers(graph, first_label=0, label_attribute='original_label')
    print(f"Nodes: {graph.number_of_nodes()}, Edges {graph.number_of_edges()}")
    source = int(random.random() * (graph.number_of_nodes() - 1))
    target = int(random.random() * (graph.number_of_nodes() - 1))
    '''if alg == 'Dijkstra':
        start = time.perf_counter()
        route, dist, iter = dijkstra(graph, source, target)
        end = time.perf_counter()
        print(f'Dijkstra route distance: {dist}\n')
        print(f'Dijkstra route finding time: {end-start}\n')
        print(f'Dijkstra search iterations: {iter}\n')
        ox.plot.plot_graph_route(nx.MultiDiGraph(graph), route)
    else:
        start = time.perf_counter()
        route, dist, iter = dijkstra(graph, source, target)
        end = time.perf_counter()
        print(f'Astar route distance: {dist}\n')
        print(f'Astar route finding time: {end-start}\n')
        print(f'Astar search iterations: {iter}\n')
        ox.plot.plot_graph_route(nx.MultiDiGraph(graph), route)'''

    d_start = time.perf_counter()
    d_route, d_dist, d_iter = dijkstra(graph, source, target)
    d_end = time.perf_counter()
    a_start = time.perf_counter()
    a_route, a_dist, a_iter = astar(graph, source, target)
    a_end = time.perf_counter()
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))
    axes[0].set_title("Dijkstra")
    axes[1].set_title("A*")
    ox.plot.plot_graph_route(nx.MultiDiGraph(graph), d_route, ax=axes[0], figsize=(10, 10), show = False, close = False, bgcolor='#111111', node_color='w', node_size=15, node_alpha=None, node_edgecolor='none', node_zorder=1, edge_color='#999999', edge_linewidth=20, edge_alpha=None, bbox=None, save=False, filepath=None, dpi=300)
    print(f'Dijkstra route distance: {d_dist}\n')
    print(f'Dijkstra route finding time: {d_end-d_start}\n')
    print(f'Dijkstra search iterations: {d_iter}\n')
    ox.plot.plot_graph_route(nx.MultiDiGraph(graph), a_route, ax=axes[1], figsize=(10, 10), show = False, close = False, bgcolor='#111111', node_color='w', node_size=15, node_alpha=None, node_edgecolor='none', node_zorder=1, edge_color='#999999', edge_linewidth=20, edge_alpha=None, bbox=None, save=False, filepath=None, dpi=300)
    print(f'Astar route distance: {a_dist}\n')
    print(f'Astar route finding time: {a_end-a_start}\n')
    print(f'Astar search iterations: {a_iter}\n')
    plt.show()

if __name__ == "__main__":
    main()