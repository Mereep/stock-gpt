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
# Brief: File Based implementation for StockValue (Chart) Repository    #
#########################################################################

from __future__ import annotations

import datetime
from pathlib import Path
from typing import Iterable

import pandas as pd

from datatypes.stock_data import StockDataInfo, StockDataChartEntry
from exceptions.repository import StockGptRepositoryException
from repository.stock_value.i_stock_value_repository import IStockValueRepository


class StockValueFileRepository(IStockValueRepository):
    _base_path: Path

    def __init__(self, base_path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not base_path.exists():
            raise StockGptRepositoryException(f'Base path {base_path} does not exist (Code: 23482039)')

        self._base_path = base_path

    def get(self, key: str) -> StockDataInfo | None:
        base_dir = self._base_path
        effective_path = base_dir / f'{key}.csv'
        if not effective_path.exists():
            return None

        df = pd.read_csv(effective_path, index_col=None, parse_dates=['date'])
        entries = {}
        for _, line in df.iterrows():
            entries[datetime.date(line['date'].year,
                                  line['date'].month,
                                  line['date'].day)] = \
                StockDataChartEntry(high=line['high'],
                                    low=line['low'],
                                    open=line['open'],
                                    close=line['close'],
                                    volume=line['volume']
                                    )

        return StockDataInfo(symbol=key, chart=entries)

    def store(self, key: str, value: StockDataInfo):
        stock_data_base_path = self._base_path
        effective_path = stock_data_base_path / f'{key}.csv'
        if not effective_path.exists():
            self.log_info(f'Creating new stock data file for symbol {key} (Code: 423840923)')
            df_old = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        else:
            self.log_info(f'Loading existing stock data file for symbol {key} (Code: 423840923)')
            df_old = pd.read_csv(effective_path, index_col=None, parse_dates=['date'])

        data_dict = {
            'date': [datetime.datetime(date.year, date.month, date.day)
                     for date in value.chart.keys()],
            'open': [entry.open for entry in value.chart.values()],
            'high': [entry.high for entry in value.chart.values()],
            'low': [entry.low for entry in value.chart.values()],
            'close': [entry.close for entry in value.chart.values()],
            'volume': [entry.volume for entry in value.chart.values()],
        }
        df_new = pd.DataFrame(columns=df_old.columns, data=data_dict, index=None)

        df_concat = pd.concat([df_new, df_old], axis=0, ignore_index=True)

        # Remove duplicates
        df_concat.drop_duplicates(subset=['date'], keep='last', inplace=True, ignore_index=True)

        # Sort by date
        df_concat.sort_values(by=['date'], inplace=True)

        # and save
        df_concat.to_csv(effective_path, index=False)

    def list_keys(self) -> Iterable[str]:
        return [path.name.replace('.csv', '') for path in
                self._base_path.iterdir() if path.is_file() and path.name.endswith('.csv')]
