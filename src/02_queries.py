# general lib
import pandas as pd
import numpy as np
# gremlin_python lib
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import T
from gremlin_python import statics
from gremlin_python.process.strategies import *



def query_01(g, alerts_unique):
    """
    calculate all vertices in degree, out degree and total degree
    :param g: graph traversal source object
    :param alerts_unique: valid unique alerts name, without None
    :return: None
    """
    print("{0:}QUERY_01{0:}".format(23 * '='))
    for elem in alerts_unique :
        id_ = g.V().has("name", elem).id().next()
        out_deg = g.V(id_).out().count().next()
        in_deg = g.V(id_).in_().count().next()
        total_deg = out_deg + in_deg
        print("{:7s}: in_degree {:2d} , out_degree {:2d}, total_degree {:2d}".format(elem, in_deg, out_deg, total_deg))
    print('\n')
    return


def query_02(g, alerts_unique):
    """
    Calculate the  directed longest chain in the graph, vertex represented by name
    :param g: graph traversal source object
    :param alerts_unique: valid unique alerts name, without None
    :return: None
    """
    # statics.load_statics(globals())
    print("{0:}QUERY_02{0:}".format(23 * '='))
    longest_chains = []
    max_chain_len = 1
    for elem in alerts_unique:
        chain = g.V().has("name", elem).repeat(__.out().simplePath()).emit().path().by("name").toList()
        if len(chain) != 0 :
            temp = chain[-1] # the returned paths are sorted in ascending order
            if len(temp) > max_chain_len:
                max_chain_len = len(temp)
                longest_chains = [temp]
            elif len(temp) == max_chain_len:
                longest_chains.append(temp)

    print("Longest chain length is {}.\nLongest Chains:".format(max_chain_len))
    for elem in longest_chains:
        print(elem)
    print('\n')
    return


def query_03(g, vertex_name = "ztf4"):
    """
    count how many vertices are connected to vertex_name(in/out)
    :param g: graph traversal source object
    :param vertex_name: type: string , the name of the vertex to query
    :return: None
    """
    print("{0:}QUERY_03{0:}".format(23 * '='))
    num = g.V().has("name", vertex_name).both().count().next()
    print("The number of vertice connected to \"{}\": {}".format(vertex_name, num))
    print("\n")
    return


def query_04(g, vertex_name = "unknown"):
    """
    extract the subgraph containing only vertics pointing to the vertex_name
    :param g: graph traversal source object
    :param vertex_name: type: string , the name of the vertex to query
    :return: subGraph
    """
    print("{0:}QUERY_04{0:}".format(23 * '='))
    # find all neighbours pointing to unknown, set property 'point_unknown' to true
    id_ = g.V().has('name', vertex_name).next()
    neighbours = g.V(id_).in_().toList() # 'ztf23' appear twice
    for idx in neighbours:
        g.V(idx).property('point_unknown', 'true').next()
    # extract the sub_graph
    sub_graph = g.withStrategies(SubgraphStrategy(vertices= __.has('point_unknown', 'true')))

    print("The sub_graph object:\n{}".format(sub_graph))
    print("The vertex map:\n {}\n".format(sub_graph.V().elementMap().toList()))
    print("The edge map:\n {}\n".format(sub_graph.E().elementMap().toList()))
    return sub_graph


if __name__ == "__main__":
    # connect gremlin server
    connection = DriverRemoteConnection("ws://localhost:8182/gremlin", "g")
    g = traversal().withRemote(connection)

    # load csv file
    alerts = pd.read_csv("../data/alerts.csv", header = None).values.squeeze()
    alerts_unique = np.unique(alerts)
    # delete entry of 'None'
    none_idx = None
    num_vertex = alerts_unique.size
    for idx in range(num_vertex):
        if alerts_unique[idx] == 'None':
            none_idx = idx
            break
    if none_idx is not None:
        alerts_unique = np.delete(alerts_unique, none_idx)
    
    # do queries:
    query_01(g, alerts_unique)
    query_02(g, alerts_unique)
    query_03(g)
    query_04(g)
    
    connection.close()