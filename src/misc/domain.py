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
# Brief: Loggers used in the project                              		#
#########################################################################
from functools import cache

from misc.config import AppConfig
from misc.utils import read_market_indicator_defaults


@cache
def get_market_indicator_name(indicator_id: str, config: AppConfig) -> str:
    """Get the name of the market indicator
    if the indicator is not found in the default dictionary, the indicator itself is returned

    :param indicator_id: the indicator to get the name for
    :param config: the app config
    :return: the name of the indicator
    """
    indicators = read_market_indicator_defaults(path_to_csv=config.default_market_indicator_dictionary_file)
    if indicator_id in indicators:
        return indicators[indicator_id]
    else:
        return indicator_id


@cache
def get_stock_indicator_name(indicator_id: str, config: AppConfig) -> str:
    """Get the name of the stock indicator
    if the indicator is not found in the default dictionary, the indicator itself is returned

    :param indicator_id: the indicator to get the name for
    :param config: the app config
    :return: the name of the indicator
    """
    indicators = read_market_indicator_defaults(path_to_csv=config.default_stock_indicator_dictionary_file)
    if indicator_id in indicators:
        return indicators[indicator_id]
    else:
        return indicator_id
