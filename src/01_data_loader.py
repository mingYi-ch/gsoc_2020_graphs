# general lib
import pandas as pd
# gremlin_python lib
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection


def load_data(g, alerts):
    """
    Read data into the graph database from csv file
    :param g: graph traversal source object
    :param alerts: two dimension numpy list, table
    :return: None
    """
    rows, cols = alerts.shape
    name_to_id = {} # record returned vertex id
    for row in range(rows):
        vals = [] # record name
        for col in range(cols):
            name = alerts[row][col]
            vals.append(name)
            if name != 'None' and name_to_id.get(name, None) == None:
                id_ = g.addV("alert").property("name", name).next()
                name_to_id[name] = id_
        # build edges between vertices
        # col3, col2 is col1
        id_0 = name_to_id.get(vals[0], None)
        id_1 = name_to_id.get(vals[1], None)
        id_2 = name_to_id.get(vals[2], None)
        if id_0 is not None:
            if id_1 is not None:
                g.addE('is').from_(id_1).to(id_0).next()
            if id_2 is not None:
                g.addE('is').from_(id_2).to(id_0).next()
        # col2 knows col3
        if id_1 is not None and id_2 is not None:
            g.addE('knows').from_(id_1).to(id_2).next()
    return


if __name__ == "__main__":
    # connect gremlin server
    connection = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g')
    g = traversal().withRemote(connection)

    # remove all vertices and edges in the graph
    g.V().drop().iterate()
    # g.E().drop().iterate()

    # populate data into graph database
    alerts = pd.read_csv('../data/alerts.csv', header = None).values
    load_data(g, alerts)
    connection.close()
    print("Data is loaded successfully.")

