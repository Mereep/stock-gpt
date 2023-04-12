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
# Brief: Interface for Indicator-Extractors                             #
#########################################################################

import abc
from datetime import datetime

from datatypes.stock_data import StockDataInfo


class IStockIndicator(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def id():
        pass

    @abc.abstractmethod
    def calculate(self, data: StockDataInfo, for_date: datetime.date) -> float:
        pass
