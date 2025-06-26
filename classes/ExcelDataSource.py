"""
Implementation of the Excel data source.
"""
from .AbstractDataSource import DataSource
import pandas as pd

class ExcelSource(DataSource):
    def __init__(self, filepath, **kwargs):
        self.filepath = filepath
        self.kwargs = kwargs

    def load(self) -> pd.DataFrame:
        return pd.read_excel(self.filepath, **self.kwargs)

class BrandHealthSource(ExcelSource):
    """
    Raw data in 'G:\\Marketing(GM)\\Marketing Strategy and Planning\\CI&CA\\Dashboard\\Marketing KPI\\Datasource (linked to Dashboard)\\BHT - Rolling 3 months KPI.xlsx' # type: ignore
    """
    def __init__(self, filepath, sheet_name='BHT Data', parse_dates=['Month'], **kwargs):
        super().__init__(filepath, sheet_name=sheet_name, parse_dates=parse_dates, **kwargs)
        self.sheet_name = sheet_name

    def load(self) -> pd.DataFrame:
        df = super().load()
        # Perform any additional processing specific to brand health data
        # Filter to keep only 2025 Marketing KPI
        df = df[df['Market'] == 'China']
        df = df[df['Brand KPI'].isin(['Brand Preference', 'TOMA', 'One-stop integrated', 'Luxurious', 'TBA'])]  # TBA for SW
        # Use 'Brand Name (EN)' column split properties, or 'Group' column to aggregate brand
        return df