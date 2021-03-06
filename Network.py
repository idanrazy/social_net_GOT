import itertools
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from networkx.algorithms.community import girvan_newman


class Network:

    """ build network and filter nodes with less then wf Weight """
    def __init__(self, path, wf=0):
        self.data_path = path
        self.Weight_filter = wf
        self.G = None
        self.Comm = None
        self.between = None

    """ create init network """
    def init_net(self):
        df = pd.read_csv(self.data_path)
        df = df.loc[df['Weight'] > self.Weight_filter]
        self.G = nx.from_pandas_edgelist(df, source="Node A", target="Node B", edge_attr=['Weight'])

    """ print net info"""
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
        print(sorted(clossnes.items(), key=lambda x: x[1], reverse=True)[:10])
        between = nx.betweenness_centrality(g)
        self.between = between
        print("top 10 Between Centrality")
        print(sorted(between.items(), key=lambda x: x[1], reverse=True)[:10])

    """ calculate communities choose iteration params of the algorithm """
    def calculate_communities(self, iter=1):
        g = self.G
        comm = girvan_newman(g)
        # first i algorithm iteration
        for communities in itertools.islice(comm, iter):
            comm_i = tuple(sorted(c) for c in communities)
            print(dict(enumerate(comm_i)))
        self.Comm = comm_i

    def link_prediction(self):
        g = self.G
        preds_jc = nx.jaccard_coefficient(g)
        pred_jc_dict = {}
        for u, v, p, in preds_jc:
            pred_jc_dict[(u, v)] = p
        result = sorted(pred_jc_dict.items(), key=lambda x:x[1], reverse=True)
        print('=' * 80)
        print("First method")
        print(result)

        preds_pa = nx.preferential_attachment(g)
        pred_pa_dict = {}
        for u, v, p in preds_pa:
            pred_pa_dict[(u, v)] = p
        result = sorted(pred_pa_dict.items(), key=lambda x:x[1], reverse=True)
        print('=' * 80)
        print("First method")
        print(result)

    def plot_network(self):
        nx.draw_spring(self.G, with_labels=True)
        plt.show()

    def plot_communities(self):
        g = self.G
        colors = ['r', 'b', 'g', 'y']
        pos = nx.spring_layout(g)
        for i in range(len(self.Comm)):
            k = g.subgraph(self.Comm[i])
            bet_size = [(self.between[node]*1000)+100 for node in k.node]
            nx.draw_networkx(k, node_color=colors[i], with_labels=True, pos=pos,node_size=bet_size)
        plt.show()
