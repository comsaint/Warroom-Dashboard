"""
Implementation of CSV source class.
"""
from .AbstractDataSource import DataSource
import pandas as pd

class CSVSource(DataSource):
    def __init__(self, filepath, **kwargs):
        self.filepath = filepath
        self.kwargs = kwargs

    def load(self) -> pd.DataFrame:
        return pd.read_csv(self.filepath, **self.kwargs)
    