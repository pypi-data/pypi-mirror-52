# info-clustering
[![PyPI](https://img.shields.io/pypi/v/info-cluster.svg)](https://pypi.org/project/info-cluster)

## Usage
```shell
pip install info-cluster
```
After installing `info-cluster` package, you can use it as follows:
```Python
from info_cluster import InfoCluster
import networkx as nx
g = nx.Graph() # undirected graph
g.add_edge(0, 1, weight=1)
g.add_edge(1, 2, weight=1)
g.add_edge(0, 2, weight=5)
ic = InfoCluster(affinity='precomputed') # use precomputed graph structure
ic.fit(g)
ic.print_hierarchical_tree()
```
The output is like
```shell
      /-0
   /-|
--|   \-2
  |
   \-1
```