import osmnx as ox 

def get_city_graph(city_string):
    graph = ""
    try:
        print("Looking for cached graph...")
        graph = ox.load_graphml(f"{city_string}.graphml")
        print("Found cached graph!")
    except:
        print("No cached graph found, downloading...")
        graph = ox.graph.graph_from_place(city_string)
        print("Saving graph to cache...")
        ox.save_graphml(graph,f"{city_string}.graphml")

    return graph


def main():
    graph = get_city_graph("Jacksonville, Florida")

    stats = ox.stats.basic_stats(graph)

    print(f"Nodes: {stats['n']}, Edges {stats['m']}")

    ox.plot.plot_graph(graph)

if __name__ == "__main__":
    main()