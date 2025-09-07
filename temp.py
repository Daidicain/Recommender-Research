import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_nodes_from(['A','B','C'], bipartite=0)
G.add_nodes_from([1,2,3,4], bipartite=1)

G.add_edges_from([('A',1, {'rating':5,'ts':9}), 
                  ('A',3, {'rating':5,'ts':0}), 
                  ('A',4, {'rating':2,'ts':5}), 
                  ('B',1, {'rating':5,'ts':9}), 
                  ('B',2, {'rating':1,'ts':1}), 
                  ('B',3, {'rating':4,'ts':8}), 
                  ('C',1, {'rating':4,'ts':1}), 
                  ('C',3, {'rating':5,'ts':4}), 
                  ('C',4, {'rating':5,'ts':1}),
                  ('D',1, {'rating':2,'ts':1}), 
                  ('D',2, {'rating':5,'ts':1}), 
                  ('D',4, {'rating':4,'ts':1}), ])



# pos = nx.bipartite_layout(G,['A','B','C'])

pos = {}
pos['A'] = (0,3)
pos['B'] = (0,2)
pos['C'] = (0,1)
pos['D'] = (0,0)

pos[1] = (1,3)
pos[2] = (1,2)
pos[3] = (1,1)
pos[4] = (1,0)

# nx.draw_networkx_nodes(G, pos ,node_color='white', edgecolors='black', linewidths=4)


nx.draw(G, pos, with_labels=True, node_color='white', edgecolors='black', linewidths=2)
nx.draw_networkx_edge_labels(G, pos, label_pos=0.2, font_size=6)
# plt.title("Bipartite Graph")
# plt.figure(facecolor='black')

plt.show()
