import rethinkdb as r
import networkx as nx
from pytictoc import TicToc


t = TicToc() #create instance of class
lo, hi = t.tic(), t.toc()

rdb = r.RethinkDB()
conn = rdb.connect(host='localhost', port=28015)

data = []
is_ok = false

feed = rdb.db('whoosh').table('graph').changes().run(conn)
for change in feed:
    indices = range(14)
    for u, v in zip(indices[:-1], indices[1:]):
    new_val = change['new_val']
    element = [
               (new_val['index'],new_val['2'],new_val['3']),
               (new_val['index'],new_val['4'],new_val['5']),
               (new_val['index'],new_val['6'],new_val['7']),
               (new_val['index'],new_val['8'],new_val['9']),
               (new_val['index'],new_val['10'],new_val['11']),
               (new_val['index'],new_val['12'],new_val['13'])
    ]

    data.extend(element)
    print('==============list', data)

print('=====TEST====', data)

# G = nx.Graph()
# G.add_weighted_edges_from(data)
#
# print(nx.dijkstra_path(G, '1', '14'))






import rethinkdb as r
import networkx as nx
from pytictoc import TicToc


t = TicToc() #create instance of class
lo, hi = t.tic(), t.toc()

rdb = r.RethinkDB()
conn = rdb.connect(host='localhost', port=28015)

is_ok = False



i = -1

while True:
    record = []
    i += 1
    data = rdb.db('whoosh').table('graph').filter({'index': i}).run(conn)

    for element in data:
        record.append(element)

    if record:
        indices = range(2, 14)
        for u, v in zip(indices[:-1], indices[1:]):
            if u % 2 != 0 and v % 2 == 0:
                continue
            print(u, v)
    else:
        break




