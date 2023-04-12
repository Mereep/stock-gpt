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
# Brief: Uncategorized utility functions                          		#
#########################################################################


from functools import cache
from pathlib import Path

import pandas as pd

from exceptions.base import StockGptException


@cache
def read_market_indicator_defaults(path_to_csv: Path) -> dict[str, str]:
    """ Reads the market indicator defaults from the given CSV file
    no check for existence of file is done (do this before calling this function)

    :param path_to_csv: The path to the CSV file (must have the columns 'id', 'name', 'active')
    :raises StockGptException: If the CSV file does not have the expected columns
    """
    return _read_default_indicators(path_to_csv)


@cache
def read_stock_indicator_defaults(path_to_csv: Path) -> dict[str, str]:
    """ Reads the stock indicator defaults from the given CSV file
    no check for existence of file is done (do this before calling this function)

    :param path_to_csv: The path to the CSV file (must have the columns 'id', 'name', 'active')
    :raises StockGptException: If the CSV file does not have the expected columns
    """
    return _read_default_indicators(path_to_csv)


def _read_default_indicators(path_to_csv: Path):
    """ reads a CSV file as a dictionary

    :param path_to_csv: The path to the CSV file (must have the columns 'id', 'name', 'active')
    :raises StockGptException: If the CSV file does not have the expected columns
    """
    file = pd.read_csv(path_to_csv, index_col=None)
    expected_columns = ['id', 'name', 'active']
    if not all(col in file.columns for col in expected_columns):
        raise StockGptException(f"CSV file {path_to_csv} does not have the "
                                f"expected columns {expected_columns} (Code: 234234)")

    d = {}
    for _, row in file.iterrows():
        if row['active']:
            d[row['id']] = row['name']

    return d
