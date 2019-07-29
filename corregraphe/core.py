import pandas as pd


def CorrelationGraph(object):
    """
    Creates a correlation graph from dataframe.

    Parameters
    ----------
    data : DataFrame
        data to use to compute correlations

    method : str = 'spearman' {'pearson', 'kendall', 'spearman'}
        correlation method, see pandas.DataFrame.corr
    """
    def __init__(self, data: pd.DataFrame, method: str = "spearman"):
        self._data = data
        self._method = method

    def draw(self):
        pass

    def _check_inputs(self):
        pass

    def _correlation(self):
        pass

    def _create_graph(self):
        pass

    def __repr__(self) -> str:
        pass
