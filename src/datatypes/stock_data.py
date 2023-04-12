#########################################################################
# {Stock GPT - Prompt Templates for LLM Stock Analysis}					#
# Copyright (C) 2023 Richard Vogel     									#
#																		#
# This program is free software: you can redistribute it and/or modify	#
# it under the terms of the GNU General Public License as published by	#
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.									#
#																		#
# This program is distributed in the hope that it will be useful,		#
# but WITHOUT ANY WARRANTY; without even the implied warranty of 		#
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 		#
# GNU General Public License for more details. 							#
# #######################################################################
# Brief: StockData Data Types (Chart)                             		#
#########################################################################

from __future__ import annotations

import dataclasses
import datetime

import pandas as pd


@dataclasses.dataclass(frozen=True)
class StockDataChartEntry:
    open: float | None = dataclasses.field(default=None)
    high: float | None = dataclasses.field(default=None)
    low: float | None = dataclasses.field(default=None)
    close: float | None = dataclasses.field(default=None)
    volume: float | None = dataclasses.field(default=None)


@dataclasses.dataclass(frozen=True)
class StockDataInfo:
    symbol: str = dataclasses.field()
    chart: dict[datetime.date, StockDataChartEntry] = dataclasses.field(default_factory=dict)

    def filter_close_dates_until(self, until_date: datetime.date):
        """ fetches all close dates until the given date

        Args:
            until_date (datetime.date): The date until which to fetch the close dates
        return (list[float]): The list of close dates
        """
        filtered = {date: entry for date, entry in self.chart.items()
                    if date <= until_date and entry.close is not None and pd.notna(entry.close)}

        return [entry.close for date, entry in filtered.items()]

    def filter_high_dates_until(self, until_date: datetime.date):
        """ fetches all high dates until the given date

        Args:
            until_date (datetime.date): The date until which to fetch the close dates
        return (list[float]): The list of close dates
        """
        filtered = {date: entry for date, entry in self.chart.items()
                    if date <= until_date and entry.high is not None and pd.notna(entry.high)}

        return [entry.high for date, entry in filtered.items()]

    def filter_low_dates_until(self, until_date: datetime.date):
        """ fetches all low dates until the given date

        Args:
            until_date (datetime.date): The date until which to fetch the close dates
        return (list[float]): The list of close dates
        """
        filtered = {date: entry for date, entry in self.chart.items()
                    if date <= until_date and entry.low is not None and pd.notna(entry.low)}

        return [entry.low for date, entry in filtered.items()]

    def filter_volumes_dates_until(self, until_date: datetime.date):
        """ fetches all volumes until the given date

        Args:
            until_date (datetime.date): The date until which to fetch the close dates
        return (list[float]): The list of close dates
        """
        filtered = {date: entry for date, entry in self.chart.items()
                    if date <= until_date and entry.volume is not None and pd.notna(entry.close)}

        return [entry.volume for date, entry in filtered.items()]

    def get_values_for_date_range(self,
                                  date_from: datetime.date,
                                  date_to: datetime.date) \
            -> dict[datetime.date, StockDataChartEntry]:
        """Gets the values for the given date range.

        Args:
            date_from (datetime.date): The start date.
            date_to (datetime.date): The end date.

        Returns:
            StockDataInfo: The stock data info for the given date range.
        """
        filtered = {date: entry for date, entry in self.chart.items()
                    if date_from <= date <= date_to and pd.notna(entry.close) and pd.notna(entry.volume) and
                    pd.notna(entry.high) and pd.notna(entry.low) and pd.notna(entry.open)}

        return filtered

    def sample_two_values_per_month(self, from_date: datetime.date) -> dict[datetime.date, StockDataChartEntry]:
        """Samples two values per month from the given date.

        Args:
            from_date (datetime.date): The date from which to sample BACKWARDS.

        Returns:
            dict[datetime.date, StockDataChartEntry]: The sampled values.
        """
        sampled = {}
        for date, entry in self.chart.items():
            if date < from_date:
                if date.day == 1 or date.day == 15:
                    sampled[date] = entry

        # sort dict by key ascending
        sampled = {k: v for k, v in sorted(sampled.items(), key=lambda item: item[0])}

        return sampled
