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
# Brief: File Based implementation for StockIndicator                   #
# (Technical) Repository                                                #
#########################################################################

from __future__ import annotations

import datetime
from pathlib import Path
from typing import Iterable

import pandas as pd

from datatypes.market_indicator import MarketIndicator
from datatypes.stock_indicator import StockIndicators
from exceptions.repository import StockGptRepositoryException
from repository.stock_indicator.i_stock_indicator_repository import IStockIndicatorRepository


class StockIndicatorFileRepository(IStockIndicatorRepository):
    _base_path: Path

    def __init__(self, base_path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not base_path.exists():
            raise StockGptRepositoryException(f'Base path {base_path} does not exist (Code: 428340923)')

        self._base_path = base_path

    def get(self, key: str) -> StockIndicators | None:
        stock_indicator_base_path = self._base_path
        effective_path = stock_indicator_base_path / f'{key}.csv'
        if effective_path.exists():
            df = pd.read_csv(effective_path, index_col=None, parse_dates=['date'])
            d = {}
            for _, line in df.iterrows():
                date = datetime.date(line['date'].year,
                                     line['date'].month,
                                     line['date'].day)
                d[date] = {}
                for col in df.columns:
                    if col != 'date':
                        d[date][col] = line[col]

            return StockIndicators(d)
        else:
            return None

    def store(self, key: str, value: StockIndicators):
        stock_indicator_base_path = self._base_path
        effective_path = stock_indicator_base_path / f'{key}.csv'
        if not effective_path.exists():
            self.log_info(f"Creating new stock indicator file for symbol {key} (Code: 423840923)")
            df_old = pd.DataFrame(columns=['date'])
        else:
            self.log_info(f"Loading existing stock indicator file for symbol {key} (Code: 423840923)")
            df_old = pd.read_csv(effective_path,
                                 index_col=None,
                                 parse_dates=['date'])

        for date, indicators in value.items():
            for indicator_id, indicator_value in indicators.items():
                if indicator_id not in df_old.columns:
                    df_old[indicator_id] = None

                # add an empty row if the date does not exist
                if date not in df_old['date'].values:
                    empty_row = [None] * (df_old.shape[1] - 1)
                    empty_row.insert(0, date)
                    df_old.loc[len(df_old)] = empty_row
                df_old.loc[df_old['date'] == date, indicator_id] = indicator_value

        df_old['date'] = [datetime.date(year=d.year, month=d.month, day=d.day) for d in df_old['date']]

        # drop duplicates
        df_old = df_old.drop_duplicates(subset=['date'], keep='last')

        # sort by date
        df_old = df_old.sort_values(by=['date'])

        # save back to disk
        df_old.to_csv(effective_path, index=False)

    def list_keys(self) -> Iterable[str]:
        return [f.name.replace('.csv', '')
                for f in self._base_path.iterdir() if f.is_file() and f.name.endswith('.csv')]
