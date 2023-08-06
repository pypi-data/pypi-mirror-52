# pylint: disable=missing-docstring

import unittest

import networkx as nx
from info_cluster import InfoCluster # pylint: disable=no-name-in-module

class TestInfoCluster(unittest.TestCase):
    def test_workflow(self):
        g = nx.Graph() # undirected graph
        g.add_edge(0, 1, weight=1)
        g.add_edge(1, 2, weight=1)
        g.add_edge(0, 2, weight=5)
        info_cluster_instance = InfoCluster(affinity='precomputed')
        info_cluster_instance.fit(g)
        info_cluster_instance.print_hierarchical_tree()
        self.assertEqual(info_cluster_instance.get_tree_depth(), 2)
    def test_4_point(self):
        g = nx.DiGraph()
        g.add_edge(0, 2, weight=2)
        g.add_edge(0, 1, weight=5)
        g.add_edge(0, 3, weight=1)
        g.add_edge(1, 2, weight=2)
        g.add_edge(1, 3, weight=1)
        info_cluster_instance = InfoCluster(affinity='precomputed')
        info_cluster_instance.fit(g)
        info_cluster_instance.print_hierarchical_tree()
        self.assertEqual(info_cluster_instance.get_tree_depth(), 3)

if __name__ == '__main__':
    unittest.main()
