# general lib
import pandas as pd
import numpy as np

def to_adjList(data_matrix):

    col0 = np.reshape(data_matrix[:, 0], (-1, 1))
    col1 = np.reshape(data_matrix[:, 1], (-1, 1))
    col2 = np.reshape(data_matrix[:, 2], (-1, 1))

    # create adjcent matrix: col1 -> col0, col1 -> col2, col2 -> col0
    adjMat_0 = np.concatenate((col1, col0, col2), axis = 1).tolist()
    adjmat_1 = np.concatenate((col2, col0), axis = 1).tolist()
    # stack two matrix
    adjMat = adjMat_0 + adjmat_1
    # remove 'None' entries
    for i in range(len(adjMat) - 1,  -1,  -1):
        row = adjMat[i]
        if row[0] == 'None':
            del adjMat[i] # the start vertex is 'None', not valid
        else:
            for j in range(len(row)):
                if row[j] == 'None':
                    del row[j]
            if len(adjMat[i]) <= 1: # no edges, delete
                del adjMat[i]
    # print(adjMat)
    df = pd.DataFrame(adjMat)
    df.to_csv("adjMatrix.csv", header = False, index = False)
    return





if __name__ == "__main__":
    # load csv file
    alerts = pd.read_csv("../data/alerts.csv", header = None).values.squeeze()
    to_adjList(alerts)