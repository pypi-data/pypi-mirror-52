# pylint: disable=cyclic-import
"""info cluster module provides InfoCluster class
"""
import numpy as np
from sklearn.metrics.pairwise import pairwise_kernels
from sklearn.neighbors import kneighbors_graph
import networkx as nx
from ete3 import Tree
from pspartition import PsPartition # pylint: disable=no-name-in-module

class InfoCluster: # pylint: disable=too-many-instance-attributes
    '''Info clustering is a kind of hierarchical clustering method.
    It computes principal sequence of partition to build the hierarchical tree.

    Parameters
    ----------
    gamma : float, default=1.0
        Kernel coefficient for rbf kernels.
    affinity : string or list, default 'rbf'
        may be one of 'precomputed', 'rbf', 'laplacian', 'nearest_neighbors'.
        if list, can only be ['rbf','nearest_neighbors'] or ['laplacian', 'nearest_neighbors']
    n_neighbors : integer
        Number of neighbors to use when constructing the affinity matrix using
        the nearest neighbors method. Ignored for ``affinity='rbf'``.
    '''
    def __init__(self, gamma=1, affinity='rbf', n_neighbors=10):
        self._gamma = gamma
        self.affinity = affinity
        self.n_neighbors = n_neighbors
        self.tree = Tree()
        self.tree_depth = 0
        self.g = None
        self.critical_values = []
        self.partition_list = []
        self.num_points = 0

    def fit(self, X, initialize_tree=True): # pylint: disable=too-many-arguments
        '''Construct an affinity graph from X using rbf kernel function,
        then applies info clustering to this affinity graph.
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            if affinity='precomputed', X is networkx like object or affinity matrix(upper triangle)
        '''
        self.tree = Tree() # clear the tree
        self._init_g(X)
        self.g.run()
        self.critical_values = self.g.get_critical_values()
        self.partition_list = self.g.get_partitions()
        self.num_points = len(self.partition_list[-1])
        if initialize_tree:
            self._get_hierachical_tree()

    def fit_predict(self, X):
        '''fit'''
        self.fit(X)

    def _add_node(self, root, node_list, num_index):
        root.add_features(cv=self.critical_values[num_index-1])
        label_list = self._partition_to_category(self.partition_list[num_index])
        cat_list = []
        for i in node_list:
            if cat_list.count(label_list[i]) == 0:
                cat_list.append(label_list[i])
        max_cat = len(cat_list)
        label_list_list = [[] for i in range(max_cat)]
        for i in node_list:
            j = cat_list.index(label_list[i])
            label_list_list[j].append(i)
        for node_list_i in label_list_list:
            node_name = ''.join([str(ii) for ii in node_list_i])
            if node_name != root.name:
                root_i = root.add_child(name=node_name)
            else:
                root_i = root
            if len(node_list_i) > 1:
                self._add_node(root_i, node_list_i, num_index+1)

    def _partition_to_category(self, partition):
        cat = np.zeros(self.num_points)
        label_index = 0
        for i in partition:
            for j in i:
                cat[j] = label_index
            label_index += 1
        return cat

    def _get_hierachical_tree(self):
        max_num = self.num_points
        node_list = [i for i in range(0, max_num)]
        self._add_node(self.tree, node_list, 1)

    def _set_tree_depth(self, node, depth):
        if node.is_leaf():
            if depth > self.tree_depth:
                self.tree_depth = depth
            return
        for node_i in node.children: # depth first search
            self._set_tree_depth(node_i, depth+1)

    def get_tree_depth(self):
        '''get clustering tree depth'''
        if self.tree.is_leaf():
            self._get_hierachical_tree()
        if self.tree_depth != 0:
            return self.tree_depth
        self._set_tree_depth(self.tree, 0)
        return self.tree_depth

    def print_hierarchical_tree(self):
        '''print the hirechical tree of clustering result
        '''
        if self.tree.is_leaf():
            self._get_hierachical_tree()
        print(self.tree)

    def get_category(self, min_num):
        '''get the clustering labels with the number of clusters no smaller than i
        Parameters
        ----------
        min_num : int, minimal number of cluster

        Returns
        --------
        list, with each element of the list denoting the label of the cluster.
        '''
        partition = self.get_partition(min_num)
        return self._partition_to_category(partition)

    def get_partition(self, min_num):
        '''
        return the index of partition whose first element is no smaller than min_num,
        '''
        for i in self.partition_list:
            if len(i) >= min_num:
                return i
        raise ValueError('cluster with min num %d not found' % min_num)

    def _init_g(self, X): # pylint: disable=too-many-branches
        is_nx_graph = False
        if isinstance(X, list):
            n_samples = len(X)
        elif isinstance(X, np.ndarray):
            n_samples = X.shape[0]
        elif isinstance(X, (nx.Graph, nx.DiGraph)):
            n_samples = nx.number_of_nodes(X)
            is_nx_graph = True
        else:
            raise TypeError('type(X) must be list, numpy.ndarray, '
                            'networkx.Graph or networkx.DiGraph')
        sim_list = []
        if not is_nx_graph:
            if self.affinity == 'precomputed':
                affinity_matrix = X
            elif self.affinity == 'nearest_neighbors':
                connectivity = kneighbors_graph(X, n_neighbors=self.n_neighbors, include_self=True)
                affinity_matrix = connectivity.todense()
            elif self.affinity == 'laplacian':
                affinity_matrix = pairwise_kernels(X, metric='laplacian', gamma=self._gamma)
            elif self.affinity == 'rbf':
                affinity_matrix = pairwise_kernels(X, metric='rbf', gamma=self._gamma)
            elif not isinstance(self.affinity, str):
                if self.affinity.count('nearest_neighbors') == 0:
                    raise ValueError("affinity list should specify nearest_neighbors")
                connectivity = kneighbors_graph(X, n_neighbors=self.n_neighbors, include_self=True)
                if self.affinity.count('laplacian') > 0:
                    affinity_matrix = pairwise_kernels(X, metric='laplacian', gamma=self._gamma)
                elif self.affinity.count('rbf') > 0:
                    affinity_matrix = pairwise_kernels(X, metric='rbf', gamma=self._gamma)
                else:
                    raise ValueError("affinity list should specify laplacian or rbf")
                affinity_matrix = np.multiply(affinity_matrix, connectivity.todense())
            else:
                raise NameError("Unknown affinity name %s" % self.affinity)
            for s_i in range(n_samples):
                for s_j in range(s_i+1, n_samples):
                    sim_list.append((s_i, s_j, affinity_matrix[s_i, s_j]))
        else:
            for s_i, s_j, weight_dic in X.edges(data=True):
                if s_i < s_j:
                    sim_list.append((s_i, s_j, weight_dic['weight']))

        self.g = PsPartition(n_samples, sim_list)
