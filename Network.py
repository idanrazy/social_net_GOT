import itertools
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from networkx.algorithms.community import girvan_newman

class Network:
    def __init__(self, path, wf=0):
        self.data_path = path
        self.Weight_filter = wf
        self.G = None
        self.Comm = None

    # create init network
    def init_net(self):
        df = pd.read_csv(self.data_path)
        df = df.loc[df['Weight'] > self.Weight_filter]
        self.G = nx.from_pandas_edgelist(df, source="Node A", target="Node B", edge_attr=['Weight'])


    def net_info(self):
        G = self.G
        print(nx.info(G))
        print("Net Denstiy: " + str(nx.density(G)))
        print("Diameter: " + str(nx.diameter(G)))
        print("Avg Clustering coefficient: " + str(nx.average_clustering(G)))

    def top10_ranked(self):
        g = self.G
        degree = nx.degree_centrality(g)
        print("top 10 degree_centrality")
        print(sorted(degree.items(), key=lambda x: x[1], reverse=True)[:10])
        clossnes = nx.closeness_centrality(g)
        print("top 10 Closeness Centrality")
        print(sorted(clossnes.items(),key=lambda x: x[1], reverse=True)[:10])
        between = nx.betweenness_centrality(g)
        print("top 10 Between Centrality")
        print(sorted(between.items(), key=lambda x: x[1], reverse=True)[:10])
        pass

    def calculate_communities(self , iter = 1):
        g = self.G
        comm = girvan_newman(g)
        # first i algorithm iteration
        for communities in itertools.islice(comm, iter):
            print(dict(enumerate(tuple(sorted(c) for c in communities))))

    def plot_network(self):
        nx.draw_spring(self.G, with_labels=True)
        plt.show()
