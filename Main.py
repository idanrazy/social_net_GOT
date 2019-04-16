import Network

path = r'data/thrones-network.csv'
if __name__ == "__main__":
    # build network and filter nodes with less then wf Weight
    net = Network.Network(path, wf=5)
    net.init_net()
    #net.plot_network()
    #net.net_info()
    #net.top10_ranked()
    net.calculate_communities(iter=3)
    net.plot_communities()