"""
Implementations of data processors for the page_metric_overview.html template.
Prepare `last_update_date`, `scorecards`, and `chart_data` (for the line chart).
"""
import pandas as pd
import datetime
from typing import Dict, Any
from .AbstractDataProcessor import AbstractPageMetricOverviewProcessor


class PropertyVisitationProcessor(AbstractPageMetricOverviewProcessor):
    """
    Process data for the Property Visitation dataset.
    """
    def process(self) -> Dict[str, Any]:
        if self.df.empty:
            result = {
                'scorecard_data': [{},],
                'chart_data': {'dates': [], 'datasets': []},
                'latest_date': 'No Data'
            }
            self._validate_output(result)
            return result
        
        # only up up the last date where all 4 visitations are available
        set_groups = {'GM Property Total', 'GM Casino Total', 'BW Property Total', 'SW Property Total'}
        interest_df = self.df[self.df['ReportGroup'].isin(set_groups)]
        group_counts_by_date = interest_df.groupby('GamingDate')['ReportGroup'].nunique()
        dates_with_all_groups = group_counts_by_date[group_counts_by_date == len(set_groups)]
        latest_date = dates_with_all_groups.index.max()

        latest_data = interest_df[interest_df['GamingDate'] == latest_date]
            
        scorecard_data = [
            {'GM Property HeadCount': f"{latest_data[latest_data['ReportGroup'] == 'GM Property Total']['Total HeadCount'].sum():,}"},
            {'GM Casino HeadCount': f"{latest_data[latest_data['ReportGroup'] == 'GM Casino Total']['Total HeadCount'].sum():,}"},
            {'BW Property HeadCount': f"{latest_data[latest_data['ReportGroup'] == 'BW Property Total']['Total HeadCount'].sum():,}"},
            {'SW Property HeadCount': f"{latest_data[latest_data['ReportGroup'] == 'SW Property Total']['Total HeadCount'].sum():,}"},
        ]

        thirty_days_ago = latest_date - datetime.timedelta(days=30)
        date_range_index = pd.date_range(start=thirty_days_ago, end=latest_date, freq='D')
        chart_data_df = interest_df[interest_df['GamingDate'].between(thirty_days_ago, latest_date)]

        pivot_df = chart_data_df.pivot_table(
            index='GamingDate',
            columns='ReportGroup',
            values='Total HeadCount',
            aggfunc='sum'
        )
        pivot_df = pivot_df.reindex(date_range_index).fillna(0)

        chart_data = {'dates': pd.to_datetime(pivot_df.index).strftime('%Y-%m-%d').tolist()}
        datasets = []
        for group in pivot_df.columns:
            datasets.append({
                'label': group,
                'data': pivot_df[group].tolist(),
                'fill': False,
                'tension': 0.1
            })
        chart_data['datasets'] = datasets

        result = {
            'scorecard_data': scorecard_data,
            'chart_data': chart_data,
            'latest_date': latest_date.strftime('%Y-%m-%d')
        }
        self._validate_output(result)
        return result
    

class BrandHealthProcessor(AbstractPageMetricOverviewProcessor):
    def process(self) -> Dict[str, Any]:
        if self.df.empty:
            result = {
                'scorecard_data': [],
                'chart_data': {'dates': [], 'datasets': []},
                'latest_date': 'No Data'
            }
            self._validate_output(result)
            return result

        # Pre-filter: China only, 2025
        self.df = self.df[self.df['Market'] == 'China']
        self.df = self.df[self.df['Month'].dt.date >= datetime.date(2025, 1, 1)]

        # prepare `latest_date``
        latest_date = self.df['Month'].max()
        latest_data = self.df[self.df['Month'] == latest_date]

        # prepare `scorecard data`
        # Use latest data of GM TOMA, BP, 2 Key Attributes, and SW TBA
        gm_latest_data = latest_data[latest_data['Brand Name (EN)'] == 'Galaxy Macau']
        sw_latest_data = latest_data[latest_data['Brand Name (EN)'] == 'StarWorld']
        scorecard_data = [
            {'GM Brand TOMA': f"{gm_latest_data[gm_latest_data['Brand KPI'] == 'TOMA']['Value'].values[0]:.1f}%"},
            {'GM Brand Preference': f"{gm_latest_data[gm_latest_data['Brand KPI'] == 'Brand Preference']['Value'].values[0]:.1f}%"},
            {'GM Key Attribute (One-stop Integrated resort)': f"{gm_latest_data[gm_latest_data['Brand KPI'] == 'One-stop integrated']['Value'].values[0]:.1f}%"},
            {'GM Key Attribute (Luxurious resort)': f"{gm_latest_data[gm_latest_data['Brand KPI'] == 'Luxurious']['Value'].values[0]:.1f}%"},
            {'SW Total Brand Awareness (aided)': f"{sw_latest_data[sw_latest_data['Brand KPI'] == 'TBA']['Value'].values[0]:.1f}%"},
        ]

        # prepare chart data
        # Use 2025 data, showing TOMA(China) of GM and selected Competitors (group level)
        chart_data_df = self.df[self.df['Brand KPI'] == 'TOMA']

        pivot_df = chart_data_df.pivot_table(
            index='Month',
            columns='Group',
            values='Value',
            aggfunc='sum'
        )

        chart_data = {'dates': pd.to_datetime(pivot_df.index).strftime('%Y %b').tolist()}
        datasets = []
        for group in pivot_df.columns:
            datasets.append({
                'label': group,
                'data': pivot_df[group].tolist(),
                'fill': False,
                'tension': 0.1
            })
        chart_data['datasets'] = datasets

        result = {
            'scorecard_data': scorecard_data,
            'chart_data': chart_data,
            'latest_date': latest_date.strftime('%Y %b')
        }
        self._validate_output(result)
        return result