import hvplot.networkx as hvnx
import networkx as nx
from pandas import DataFrame
from typing import Dict, Tuple


def CorrelationGraph(object):
    """
    Creates a correlation graph from dataframe.

    Parameters
    ----------
    data : DataFrame
        data to use to compute correlations

    method : str = 'kendall' {'pearson', 'kendall', 'spearman'}
        correlation method, see pandas.DataFrame.corr
    """

    def __init__(self, data: DataFrame, method: str = "kendall"):
        self._data = data
        self._method = method
        self.correlations = self._compute_correlations(self._data, self._method)
        self.graph, self.pos = self._create_graph(self.correlations)

    def draw(self, **kwargs):
        return hvnx.draw(
            self.graph,
            pos=self.pos,
            edge_width="weight",
            node_color="weight",
            labels="name",
            colorbar=True,
            **kwargs
        )

    @staticmethod
    def _compute_correlations(data: DataFrame, method: str) -> DataFrame:
        return data.corr(method=method).abs()

    @staticmethod
    def _create_graph(correlations: DataFrame) -> Tuple[nx.Graph, Dict]:
        graph = nx.complete_graph(correlations.shape[1])
        graph = nx.relabel_nodes(
            graph, {i: col for i, col in enumerate(correlations.columns)}
        )

        for edge in graph.edges:
            graph.edges[edge]["weight"] = correlations[edge[0]][edge[1]]

        for node in graph.nodes:
            graph.nodes[node]["name"] = node

        pos = nx.spring_layout(graph)

        for node, coef in nx.clustering(graph, weight="weight").items():
            graph.nodes[node]["weight"] = coef
        return graph, pos

    def __repr__(self) -> str:
        pass
