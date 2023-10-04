import math

import rethinkdb as r
import networkx as nx
from pytictoc import TicToc
import uuid

rdb = r.RethinkDB()
conn = rdb.connect(host='rethinkdb', port=28015)


def generate_id():
    return uuid.uuid4()


def dist(a, b):
    return math.sqrt((a["lat"] - b["0"]) * (a["lat"] - b["0"]) + (a["lon"] - b["1"]) * (a["lon"] - b["1"]))


def calculate_dijkstra(table_id,point_start, point_finish):
    nodes = []
    node_id_start = ''
    node_id_finish = ''
    i = -1
    while True:
        record = []
        i += 1

        data = rdb.db('whoosh').table('graph').filter({'index': i}).run(conn)

        for element in data:

            if dist(point_start, element) < 0.0001:
                node_id_start = element['index']
            if dist(point_finish, element) < 0.0001:
                node_id_finish = element['index']
            record.append(element)
        if record:
            for node_graph in record:
                indices = range(2, 14)
                for u, v in zip(indices[:-1], indices[1:]):
                    if u % 2 != 0 and v % 2 == 0:
                        continue

                    nodes.append((str(node_graph['index']), str(node_graph[str(u)]), node_graph[str(v)]))
        else:
            break

    G = nx.Graph()
    G.add_weighted_edges_from(nodes)
    #
    return nx.dijkstra_path(G, str(node_id_start), str(node_id_finish))


def calculate_path(table_id,point_start,point_finish):
    dijkstra_result = str(calculate_dijkstra(table_id,
                                             point_start,
                                             point_finish))

    rdb.db('whoosh').table(str(table_id)).insert(
        {'result': dijkstra_result
         }).run(conn)


