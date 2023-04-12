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
# Brief: Summary-like information DataClass for a Stock Symbol   		#
#########################################################################
from dataclasses import dataclass


@dataclass(frozen=True)
class StockInfo:
    name: str
    sectors: list[str]
    market_cap: float
    pe_ratio: float
    dividend_yield: float
    beta: float
    high_52_week: float
    low_52_week: float
    eps: float
