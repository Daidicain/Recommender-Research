import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

S = ['S\u2081',
     'S\u2082',
     'S\u2083',
     'S\u2084',
     'S\u2085',
     'S\u2086']
CX = ['CX\u2081',
      'CX\u2082']

G.add_nodes_from(S, bipartite=0)
G.add_nodes_from(CX, bipartite=1)

G.add_edges_from([(S[0], CX[0], {'weight':'2/5'}), 
                  (S[0], CX[1], {'weight':'4/5'}), 
                  (S[1], CX[1], {'weight':'1/6'}), 
                  (S[2], CX[0], {'weight':'1/5'}), 
                  (S[2], CX[1], {'weight':'1/6'}), 
                  (S[3], CX[0], {'weight':'2/5'}), 
                  (S[3], CX[1], {'weight':'1/7'}), 
                  (S[4], CX[1], {'weight':'1/6'}), 
                  (S[5], CX[0], {'weight':'1/4'}), 
  

                  
                  ])

# print('\u&#8528')

# pos = nx.bipartite_layout(G,['A','B','C'])

pos = {}
pos[S[0]] = (1,1)
pos[S[1]] = (2,1)
pos[S[2]] = (3,1)
pos[S[3]] = (4,1)
pos[S[4]] = (5,1)
pos[S[5]] = (6,1)


pos[CX[0]] = (2.5,0)
pos[CX[1]] = (4.5,0)


# nx.draw_networkx_nodes(G, pos ,node_color='white', edgecolors='black', linewidths=4)


nx.draw(G, pos, node_size=1500, font_size=22, with_labels=True, node_color='white', edgecolors='black', linewidths=2)

labels = nx.get_edge_attributes(G, 'weight')

nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, label_pos=0.2, font_size=12)
# plt.title("Bipartite Graph")
# plt.figure(facecolor='black')

plt.show()
