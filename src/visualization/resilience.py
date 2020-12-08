# This file performs a targeted and random attacks on the PIRA network in each period.
# These attacks are to assess the resilience of the network over time.

import pandas as pd
import networkx as nx
import operator
import random
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")




def sizeGCC(G):
    # Returns the size of the giant connected component (GCC) as a percentage of the overall network.
    CC = sorted(nx.connected_components(G), key=len, reverse=True)
    GCC = G.subgraph(CC[0])
    return (len(GCC.nodes())/float(len(G.nodes())))


def remove_nodes(G, n, node_list):
    # Removes the first n nodes in node_list from the network.
    for j in node_list[0:n]:
        G.remove_node(j[0])
    return G


def remove_random_nodes(G, n):
    # Removes n nodes at random from the network.
    for j in range(n):
        node = random.randint(0,len(G.nodes())-1)
        G.remove_node(list(G.nodes())[node])
    return G


def targeted_attack(network, iterations, nodes_per_iteration):
    # Targeted attack on the network that removes nodes based on degree centrality.
    
    network_under_attack = network.copy(as_view = False)
    nodes_removed = []
    percentage_size_of_GCC = []
    
    # Removes "nodes_per_iteration" number of nodes per loop.
    for j in range(iterations):
        nodes_removed.append(j*nodes_per_iteration)
        percentage_size_of_GCC.append(sizeGCC(network_under_attack))
        
        if sizeGCC(network_under_attack) > 0:
            sorted_by_degree = sorted(dict(network_under_attack.degree()).items(), reverse = True, key = operator.itemgetter(1))
            remove_nodes(network_under_attack, nodes_per_iteration, sorted_by_degree)
    
    # Storing details about the attack in a dataframe.
    attack_df = pd.DataFrame(data = {"Attack_Type":"Targeted", "Nodes_Removed":nodes_removed, "GCC_Percentage_Size":percentage_size_of_GCC})
    return attack_df


def random_attack(network, iterations, nodes_per_iteration):
    # Random attack on the network.
    
    network_under_attack = network.copy(as_view = False)
    nodes_removed = []
    percentage_size_of_GCC = []
    
    # Removes "nodes_per_iteration" number of nodes per loop.
    for j in range(iterations):
        nodes_removed.append(j*nodes_per_iteration)
        percentage_size_of_GCC.append(sizeGCC(network_under_attack))
        
        if sizeGCC(network_under_attack) > 0:
            remove_random_nodes(network_under_attack, nodes_per_iteration)
    
    # Storing details about the attack in a dataframe.
    attack_df = pd.DataFrame(data = {"Attack_Type":"Random", "Nodes_Removed":nodes_removed, "GCC_Percentage_Size":percentage_size_of_GCC})
    return attack_df




# PIRA Networks
p1 = pd.read_csv("https://raw.githubusercontent.com/powerd4/SNA_project/master/data/raw/PIRA%20Gill%20CSV/CSV/60_PERIOD1_NET.csv", index_col=0)
p2 = pd.read_csv("https://raw.githubusercontent.com/powerd4/SNA_project/master/data/raw/PIRA%20Gill%20CSV/CSV/60_PERIOD2_NET.csv", index_col=0)
p3 = pd.read_csv("https://raw.githubusercontent.com/powerd4/SNA_project/master/data/raw/PIRA%20Gill%20CSV/CSV/60_PERIOD3_NET.csv", index_col=0)
p4_5 = pd.read_csv("https://raw.githubusercontent.com/powerd4/SNA_project/master/data/raw/PIRA%20Gill%20CSV/CSV/60_PERIOD4_5_NET.csv", index_col=0)
p6 = pd.read_csv("https://raw.githubusercontent.com/powerd4/SNA_project/master/data/raw/PIRA%20Gill%20CSV/CSV/60_PERIOD6_NET.csv", index_col=0)

G1 = nx.from_pandas_adjacency(p1)
G2 = nx.from_pandas_adjacency(p2)
G3 = nx.from_pandas_adjacency(p3)
G4_5 = nx.from_pandas_adjacency(p4_5)
G6 = nx.from_pandas_adjacency(p6)




# Targeted Attacks
period_1_tgt_attack = targeted_attack(network = G1, iterations = 33, nodes_per_iteration = 10)
period_2_tgt_attack = targeted_attack(network = G2, iterations = 26, nodes_per_iteration = 10)
period_3_tgt_attack = targeted_attack(network = G3, iterations = 52, nodes_per_iteration = 10)
period_4_5_tgt_attack = targeted_attack(network = G4_5, iterations = 36, nodes_per_iteration = 10)
period_6_tgt_attack = targeted_attack(network = G6, iterations = 8, nodes_per_iteration = 10)

# Random Attacks
period_1_rand_attack = random_attack(network = G1, iterations = 33, nodes_per_iteration = 10)
period_2_rand_attack = random_attack(network = G2, iterations = 26, nodes_per_iteration = 10)
period_3_rand_attack = random_attack(network = G3, iterations = 52, nodes_per_iteration = 10)
period_4_5_rand_attack = random_attack(network = G4_5, iterations = 36, nodes_per_iteration = 10)
period_6_rand_attack = random_attack(network = G6, iterations = 8, nodes_per_iteration = 10)

# Attack Information per Period
period_1_df = pd.concat([period_1_tgt_attack, period_1_rand_attack], axis = 0, ignore_index = True)
period_2_df = pd.concat([period_2_tgt_attack, period_2_rand_attack], axis = 0, ignore_index = True)
period_3_df = pd.concat([period_3_tgt_attack, period_3_rand_attack], axis = 0, ignore_index = True)
period_4_5_df = pd.concat([period_4_5_tgt_attack, period_4_5_rand_attack], axis = 0, ignore_index = True)
period_6_df = pd.concat([period_6_tgt_attack, period_6_rand_attack], axis = 0, ignore_index = True)




# Plots of the Network Attacks for each Period
def network_attack_plot(data, period):
    ax = sns.lineplot(data = data, x = "Nodes_Removed", y = "GCC_Percentage_Size", hue = "Attack_Type")
    
    legend = ax.legend(loc = "upper right")
    legend.texts[0].set_text("Attack Type")
    
    ax.set_title("Period " + str(period) + " Attack")
    ax.set_ylabel("Size of GCC (% of total nodes)")
    ax.set_xlabel("Number of Nodes Removed")
    
    return ax


period_1_plot = network_attack_plot(data = period_1_df, period = 1)
plt.show()

period_2_plot = network_attack_plot(data = period_2_df, period = 2)
plt.show()

period_3_plot = network_attack_plot(data = period_3_df, period = 3)
plt.show()

period_4_5_plot = network_attack_plot(data = period_4_5_df, period = "4/5")
plt.show()

period_6_plot = network_attack_plot(data = period_6_df, period = 6)
plt.show()
