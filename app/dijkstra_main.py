import rethinkdb as r
import networkx as nx
from pytictoc import TicToc


t = TicToc() #create instance of class
lo, hi = t.tic(), t.toc()

rdb = r.RethinkDB()
conn = rdb.connect(host='localhost', port=28015)

is_ok = False



i = -1
nodes = []
while True:
    record = []
    i += 1
    data = rdb.db('whoosh').table('graph').filter({'index': i}).run(conn)

    for element in data:
        record.append(element)

    if record:
        for node_graph in record:
            indices = range(2, 14)
            for u, v in zip(indices[:-1], indices[1:]):
                if u % 2 != 0 and v % 2 == 0:
                    continue

                nodes.append((str(node_graph['index']),str(node_graph[str(u)]),node_graph[str(v)]))
    else:
        break

G = nx.Graph()
G.add_weighted_edges_from(nodes)
#
print(nx.dijkstra_path(G, '1', '14'))
