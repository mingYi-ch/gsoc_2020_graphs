# GSoC 2020: Proposed Solution for Evaluation

This repository contains my solution to the GSoC 2020: Evaluation submission.

## Prerequistes and Installation

### Install Python library

Python 3.6.5. The libraries required are `pandas`, `gremlin_python`, `numpy`

### Install docker
Docker version 2.2.0.4(43472)

### Install Gremlin Client and Server
Run Gremlin server and client in docker container.<br />
```
>> docker run -it -p 8182:8182 janusgraph/janusgraph
```

Following Commands are used to open a gremlin server console in terminal, but not required for running the python code<br />
```
>> docker container ls  
>> docker exec -it [container-id] bash  
>> bin/gremlin.sh   
>> :remote connect tinkerpop.server conf/remote.yaml  
>> :remote console 
```

Reference instruction [Gremlin\_docker\_install](https://docs.janusgraph.org/getting-started/installation/) 
## Proposed Solution
`query_result` file contains the output of the queries

### Solution 1: building the graph

Run `01_data_loader.py` to load the data in csv file.

### Solution 2: manipulation of the graph
Run `02_queries.py` to print out the results of the queries.

### Solution 3: visualisation of the graph
The img floder contains the graph picture.
