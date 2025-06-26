"""
Base class for data processor, to process data for the HTML templates.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import pandas as pd

class AbstractPageMetricOverviewProcessor(ABC):
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    @abstractmethod
    def process(self) -> Dict[str, Any]:
        """
        必須回傳一個 dict，包含 'scorecard_data', 'chart_data', 'latest_date' 三個 key。
        `scorecard_data` is a list of dicts, each dict represents a score.
        `chart_data` is a dict with 'dates' and 'datasets' keys.
        `latest_date` is a string of a date, or None if no date.
        """
        pass

    def _validate_output(self, result: Dict[str, Any]):
        # 強制必須有這三個 key
        required_keys = {'scorecard_data', 'chart_data', 'latest_date'}
        if set(result.keys()) != required_keys:
            raise ValueError(f"Output dict keys must be {required_keys}, got {set(result.keys())}")

        # 強制型別
        if not isinstance(result['scorecard_data'], list):
            raise TypeError("scorecard_data must be a dict")
        if not isinstance(result['chart_data'], dict):
            raise TypeError("chart_data must be a dict")
        if not (isinstance(result['latest_date'], str) or result['latest_date'] is None):
            raise TypeError("latest_date must be a string or None")

# define abstract processor for other HTML templates
    