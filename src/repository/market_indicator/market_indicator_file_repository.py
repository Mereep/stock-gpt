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
# Brief: File Based implementation for MarketIndicator Repository       #
#########################################################################

from __future__ import annotations

import datetime
from pathlib import Path
from typing import Iterable

import pandas as pd

from datatypes.market_indicator import MarketIndicator
from exceptions.repository import StockGptRepositoryException
from repository.market_indicator.i_market_indicator_repository import IMarketIndicatorRepository


class MarketIndicatorFileRepository(IMarketIndicatorRepository):
    _base_path: Path

    def __init__(self, base_path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not base_path.exists():
            raise StockGptRepositoryException(f'Base path {base_path} does not exist (Code: 324823)')

        self._base_path = base_path

    def get(self, key: str) -> MarketIndicator | None:
        file_path = self._base_path / f'{key}.csv'
        if file_path.exists():
            d = {}
            df = pd.read_csv(file_path, index_col=None, parse_dates=['date'])
            for _, line in df.iterrows():
                try:
                    val = float(line['value'])
                except (ValueError, TypeError):
                    val = None

                d[datetime.date(line['date'].year,
                                line['date'].month,
                                line['date'].day)] = val

            return MarketIndicator(d)
        else:
            return None

    def store(self, key: str, value: MarketIndicator):
        file_path = self._base_path / f'{key}.csv'
        if file_path.exists():
            # load old data
            df_old = pd.read_csv(file_path, index_col=None, parse_dates=['date'])
            self.log_info(f"Updating indicator {key} (Code: 34823904)")
        else:
            # create empty dataframe
            df_old = pd.DataFrame(columns=['date', 'value'])
            self.log_info(f"Creating indicator {key} (Code: 320498239)")

        # append new data
        dates = list(value.keys())
        values = list(value.values())
        df_new = pd.DataFrame({'date': dates, 'value': values})

        df_concat = pd.concat([df_old, df_new], axis=0, ignore_index=True)

        # remove duplicates
        df_concat.drop_duplicates(subset=['date'], inplace=True, keep='last')

        # sort by date
        df_concat['date'] = [datetime.date(year=d.year, month=d.month, day=d.day)
                             for d in df_concat['date']]
        df_concat.sort_values(by=['date'], inplace=True)

        # ... and save
        df_concat.to_csv(file_path, index=False)

    def list_keys(self) -> Iterable[str]:
        return [path.name.replace('.csv', '') for path in
                self._base_path.iterdir() if path.is_file() and path.name.endswith('.csv')]
