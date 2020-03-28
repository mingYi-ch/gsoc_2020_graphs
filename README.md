# GSoC 2020: Proposed Solution for Evaluation

This repository contains my solution to the GSoC 2020: Evaluation submission.

## Prerequistes and Installation

### Install Python library

Python 3.6.5. The libraries required are `pandas`, `gremlin_python`, `numpy`

### Install and Run HBase locally
Install [HBase](https://hbase.apache.org/book.html#quickstart), the version used in solution file is 2.2.3, default settings <br />
Run HBase
```
bin/start-hbase.sh
```
HBase Web UI  `http://localhost:16010`

### Install JanusGraph Server and Connect HBase
Install [janusgraph-full-0.5.1](https://github.com/JanusGraph/janusgraph/releases)<br />
Run the following commands in the downloaded folder to set up HBase connection
```
>> bin/janusgraph.sh start
>> bin/gremlin.sh   
>> :remote connect tinkerpop.server conf/remote.yaml  
>> :remote console 
>> JanusGraph graph = JanusGraphFactory.build().set('storage.backend', 'hbase').open()
>> graph = JanusGraphFactory.open('conf/janusgraph-hbase-es.properties')
```
Reference Instruction [JanusGraph Server](https://docs.janusgraph.org/basics/server/)

## Proposed Solution
`query_result` file contains the output of the queries

### Solution 1: building the graph

Run `01_data_loader.py` to load the data in csv file.

### Solution 2: manipulation of the graph
Run `02_queries.py` to print out the results of the queries.

### Solution 3: visualisation of the graph
The img floder contains the graph picture.
