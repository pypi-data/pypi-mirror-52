# pylint: disable=missing-docstring

from unittest import TestCase

import networkx as nx
from info_cluster import InfoCluster # pylint: disable=no-name-in-module

class TestInfoCluster(TestCase):
    def test_workflow(self):
        g = nx.Graph() # undirected graph
        g.add_edge(0, 1, weight=1)
        g.add_edge(1, 2, weight=1)
        g.add_edge(0, 2, weight=5)
        info_cluster_instance = InfoCluster(affinity='precomputed')
        info_cluster_instance.fit(g)
        info_cluster_instance.print_hierarchical_tree()
        self.assertEqual(info_cluster_instance.get_tree_depth(), 3)
