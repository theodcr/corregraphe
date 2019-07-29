from typing import Dict

import hvplot.networkx as hvnx
import networkx as nx
from holoviews import Overlay
from pandas import DataFrame


class CorrelationGraph(object):
    """
    Creates a correlation graph from dataframe.

    Parameters
    ----------
    data : DataFrame
        data to use to compute correlations

    method : str = 'kendall' {'pearson', 'kendall', 'spearman'}
        correlation method, see pandas.DataFrame.corr

    Attributes
    ----------
    correlations : DataFrame
        dataframe of correlations, columns and indexes are columns of `data`
    graph : Graph
        NetworkX graph object representing the correlations,
        each node is a column of `data`, edges are correlations
    pos : Dict
        positions of nodes, keys are node names, value are (x, y) positions

    Usage
    -----
    >>> df = DataFrame({'a': [1, 2, 3, 4], 'b': [2, 4, 6, 8]})
    >>> cg = CorrelationGraph(df)
    >>> cg.correlations
         a    b
    a  1.0  1.0
    b  1.0  1.0
    >>> fig = cg.draw()
    """

    def __init__(self, data: DataFrame, method: str = "kendall") -> None:
        self._data = data
        self._method = method
        self.correlations = self._compute_correlations(self._data, self._method)
        self.graph = self._create_graph(self.correlations)
        self.pos = self._compute_positions(self.graph)

    def draw(self, **kwargs) -> Overlay:
        """Draws the graph and returns the hvplot object.

        Keyword arguments are given to the hvplot.networkx.draw method.

        Returns
        -------
        Overlay
            HoloViews Overlay representing the correlation graph
        """
        return hvnx.draw(
            self.graph,
            pos=self.pos,
            edge_width="correlation",
            node_color="weight",
            labels="name",
            colorbar=True,
            **kwargs
        )

    @staticmethod
    def _compute_correlations(data: DataFrame, method: str) -> DataFrame:
        """Computes correlation between columns of dataframe.

        Parameters
        ----------
        data : DataFrame
        method : str
            correlation method

        Returns
        -------
        DataFrame
            dataframe of correlations, columns and indexes are columns of `data`
        """
        return data.corr(method=method).abs()

    @staticmethod
    def _create_graph(correlations: DataFrame) -> nx.Graph:
        """Creates a graph object to represent correlations.

        Parameters
        ----------
        correlations : DataFrame
            square dataframe of correlations, columns and indexes must be identical

        Returns
        -------
        Graph
            NetworkX graph object representing the correlations
        """
        graph = nx.complete_graph(correlations.shape[1])
        graph = nx.relabel_nodes(
            graph, {i: col for i, col in enumerate(correlations.columns)}
        )

        for edge in graph.edges:
            graph.edges[edge]["correlation"] = correlations[edge[0]][edge[1]]

        for node in graph.nodes:
            graph.nodes[node]["name"] = node

        for node, coef in nx.clustering(graph, weight="correlation").items():
            graph.nodes[node]["weight"] = coef

        return graph

    @staticmethod
    def _compute_positions(graph: nx.Graph) -> Dict:
        """Returns positions of nodes using a spring layout.

        Parameters
        ----------
        graph : Graph
            correlation graph, each node is a column, each link is a correlation

        Returns
        -------
        Dict
            positions of nodes, keys are node names, value are (x, y) positions
        """
        return nx.spring_layout(graph)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
