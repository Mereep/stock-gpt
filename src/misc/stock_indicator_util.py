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
# Brief: Utility Methods for stock indicators                     		#
#########################################################################
from __future__ import annotations

import inspect
from typing import Type

from stock_indicators.i_indicator import IStockIndicator
import stock_indicators.indicator_impl as indicator_module


def get_stock_indicator_by_id(id) -> Type[IStockIndicator] | None:
    """ will find a stock indicator by its id if available

    Args:
        id (str): the id of the indicator to find
    Returns:
        IStockIndicator | None: the indicator if found or None
    """
    # find all classes in the indicator module
    classes = inspect.getmembers(indicator_module, inspect.isclass)
    # filter the classes to only include the stock indicators
    stock_indicators = [c for c in classes if issubclass(c[1], IStockIndicator)]
    # find the indicator with the given id
    indicator = next((i for i in stock_indicators if i[1].id() == id), None)

    return indicator[1] if indicator else None
