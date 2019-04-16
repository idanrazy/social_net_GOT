import Network

path = r'data/thrones-network.csv'
if __name__ == "__main__":
    net = Network.Network(path, wf=0)
    net.init_net()
    #net.net_info()
    #net.top10_ranked()
    net.calculate_communities(iter=3)
    net.plot_communites()